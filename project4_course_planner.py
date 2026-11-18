from collections import defaultdict, deque

class CoursePlanner:
    def __init__(self):
        self.adj = defaultdict(list)
        self.courses = set()

    def add_prerequisite(self, prereq, course):
        self.adj[prereq].append(course)
        self.courses.add(prereq)
        self.courses.add(course)

    def detect_cycles_and_plan(self):
        color = {c: 0 for c in self.courses}
        topo_order = []
        cycle_detected = False
        cycle_edge = None

        def dfs_visit(u):
            nonlocal cycle_detected, cycle_edge
            color[u] = 1
            
            for v in self.adj[u]:
                if color[v] == 1:
                    cycle_detected = True
                    cycle_edge = (u, v)
                    return
                elif color[v] == 0:
                    dfs_visit(v)
                    if cycle_detected:
                        return
                        
            color[u] = 2
            topo_order.append(u)

        for course in sorted(list(self.courses)):
            if color[course] == 0:
                dfs_visit(course)
                if cycle_detected:
                    break

        if cycle_detected:
            return None, f"Cycle detected: {cycle_edge[0]} -> {cycle_edge[1]}"
        else:
            return topo_order[::-1], "Valid DAG plan."

    def calculate_semester_levels(self):
        in_degree = {c: 0 for c in self.courses}
        for u in self.adj:
            for v in self.adj[u]:
                in_degree[v] += 1

        queue = deque([c for c in self.courses if in_degree[c] == 0])
        semesters = []

        while queue:
            current_level = []
            for _ in range(len(queue)):
                u = queue.popleft()
                current_level.append(u)
                for v in self.adj[u]:
                    in_degree[v] -= 1
                    if in_degree[v] == 0:
                        queue.append(v)
            semesters.append(current_level)

        return semesters

def demo_course_planner():
    planner = CoursePlanner()
    planner.add_prerequisite("CS101_Prog1", "CS102_DataStruct")
    planner.add_prerequisite("CS102_DataStruct", "CS314_Algorithms")
    planner.add_prerequisite("MATH101_Calc1", "MATH201_Calc2")
    planner.add_prerequisite("MATH201_Calc2", "CS314_Algorithms")
    planner.add_prerequisite("CS314_Algorithms", "CS401_AI")
    planner.add_prerequisite("CS314_Algorithms", "CS402_Compilers")

    print(">>> 1. Testing Valid Curriculum Plan:")
    order, msg = planner.detect_cycles_and_plan()
    print(f"Status: {msg}")
    print(f"Topological Order: {' -> '.join(order)}")
    
    print("\n>>> Semesters by Levels:")
    semesters = planner.calculate_semester_levels()
    for idx, sem in enumerate(semesters, start=1):
        print(f"  Semester {idx}: {sem}")

    print("\n" + "=" * 60)
    print(">>> 2. Testing Invalid Curriculum Plan with Circular Dependency:")
    broken_planner = CoursePlanner()
    broken_planner.add_prerequisite("A", "B")
    broken_planner.add_prerequisite("B", "C")
    broken_planner.add_prerequisite("C", "A")
    broken_order, broken_msg = broken_planner.detect_cycles_and_plan()
    print(f"Status: {broken_msg}")

if __name__ == "__main__":
    demo_course_planner()
