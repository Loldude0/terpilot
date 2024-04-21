class DirectionalGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)

    def get_adjacent(self, u):
        return self.graph.get(u, [])

    def __str__(self):
        return str(self.graph)

    def __repr__(self):
        return str(self.graph)
    
class CoursePrerequisiteGraph(DirectionalGraph):
    def __init__(self):
        super().__init__()
        self.satisfied = {}
    
    def add_prerequisite(self, course, prerequisite):
        self.add_edge(course, prerequisite)
        self.is_satisfied[course] = False
    
    def mark_satisfied(self, course):
        self.satisfied[course] = True

    def get_prerequisites(self, course):
        return self.get_adjacent(course)
    
    def is_satisfied(self,course):
        for prereq in self.get_prerequisites(course):
            if not self.satisfied[prereq]:
                return False
        return True
        
    def __str__(self):
        return str(self.graph)

    def __repr__(self):
        return str(self.graph)