import random
import time

class MockEnvironment:
    """Simulates the outside world that the agent interacts with."""
    def __init__(self):
        self.weather = "Clear"
        self.budget = 500

    def update(self):
        # 30% chance the weather turns bad while the agent is planning
        self.weather = "Rain" if random.random() < 0.3 else "Clear"

class GoalAgent:
    def __init__(self, goal):
        self.goal = goal
        self.state = {"completed": [], "current_budget": 500}
        self.tasks = {}
        self.env = MockEnvironment()

    def decompose_goal(self):
        """Hardcoded task graph with dependencies and costs."""
        self.tasks = {
            "research": {"name": "Research destinations", "depends_on": [], "cost": 0, "status": "pending", "retries": 0},
            "check_weather": {"name": "Check local weather", "depends_on": ["research"], "cost": 0, "status": "pending", "retries": 0},
            "book_tickets": {"name": "Book flight tickets", "depends_on": ["check_weather"], "cost": 200, "status": "pending", "retries": 0},
            "pack": {"name": "Pack bags", "depends_on": ["book_tickets"], "cost": 0, "status": "pending", "retries": 0}
        }

    def get_valid_actions(self):
        """Returns a list of task IDs whose dependencies are fully met."""
        valid = []
        for task_id, info in self.tasks.items():
            if info["status"] != "pending":
                continue
            
            # Check if all dependencies are marked as 'completed'
            can_do = all(self.tasks[dep]["status"] == "completed" for dep in info["depends_on"])
            if can_do:
                valid.append(task_id)
        return valid

    def action_score(self, task_id):
        """
        Calculates utility. 
        Higher score means it should be executed first.
        """
        task = self.tasks[task_id]
        # Simple heuristic: Prioritize cheaper tasks to save budget
        score = 100 - task["cost"] 
        return score

    def execute(self, task_id):
        """Attempts to perform the action and interacts with the mock environment."""
        task = self.tasks[task_id]
        print(f"\n[Agent] Attempting: {task['name']}...")
        time.sleep(1) # Simulate processing time
        
        # The environment shifts slightly every time an action is taken
        self.env.update()
        
        # Specific task logic & failure conditions
        if task_id == "book_tickets":
            if self.env.weather == "Rain":
                print("  -> FAILURE: Weather is bad! Waiting for it to clear up.")
                return False
            if self.state["current_budget"] < task["cost"]:
                print("  -> FAILURE: Insufficient funds!")
                return False
            
            self.state["current_budget"] -= task["cost"]
            print(f"  -> Budget updated: ${self.state['current_budget']} remaining.")
            
        print(f"  -> SUCCESS: '{task['name']}' completed.")
        return True

    def act(self):
        """The main execution loop."""
        print(f"=== Starting Goal: {self.goal} ===")
        self.decompose_goal()
        
        while True:
            valid_actions = self.get_valid_actions()
            
            # End conditions
            if not valid_actions:
                if all(t["status"] == "completed" for t in self.tasks.values()):
                    print("\n=== GOAL ACHIEVED! ===")
                else:
                    print("\n=== AGENT STUCK: Cannot reach goal. ===")
                break
                
            # Pick the best action based on the scoring function
            best_action = max(valid_actions, key=self.action_score)
            
            # Execute and handle the result
            success = self.execute(best_action)
            
            if success:
                self.tasks[best_action]["status"] = "completed"
                self.state["completed"].append(best_action)
            else:
                print("  -> [Agent] Replanning/Retrying required...")
                self.tasks[best_action]["retries"] += 1
                
                # Prevent infinite loops if the environment stays bad
                if self.tasks[best_action]["retries"] >= 3:
                    print(f"  -> [Agent] Task '{self.tasks[best_action]['name']}' failed too many times. Aborting.")
                    self.tasks[best_action]["status"] = "failed"