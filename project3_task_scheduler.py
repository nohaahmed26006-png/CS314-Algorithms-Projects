class Task:
    def __init__(self, task_id, name, priority):
        self.task_id = task_id
        self.name = name
        self.priority = priority
        self.wait_time = 0

    def __repr__(self):
        return f"[ID:{self.task_id} {self.name} | Prio:{self.priority} | Wait:{self.wait_time}t]"

class MaxHeapPriorityQueue:
    def __init__(self):
        self.heap = []

    def _parent(self, i): return (i - 1) // 2
    def _left(self, i):   return 2 * i + 1
    def _right(self, i):  return 2 * i + 2

    def _max_heapify(self, i):
        largest = i
        l = self._left(i)
        r = self._right(i)
        n = len(self.heap)

        if l < n and self.heap[l].priority > self.heap[largest].priority:
            largest = l
        if r < n and self.heap[r].priority > self.heap[largest].priority:
            largest = r

        if largest != i:
            self.heap[i], self.heap[largest] = self.heap[largest], self.heap[i]
            self._max_heapify(largest)

    def insert(self, task):
        self.heap.append(task)
        i = len(self.heap) - 1
        while i > 0 and self.heap[self._parent(i)].priority < self.heap[i].priority:
            p = self._parent(i)
            self.heap[i], self.heap[p] = self.heap[p], self.heap[i]
            i = p

    def extract_max(self):
        if not self.heap:
            return None
        max_task = self.heap[0]
        last_item = self.heap.pop()
        if self.heap:
            self.heap[0] = last_item
            self._max_heapify(0)
        return max_task

    def apply_aging(self, aging_threshold=2, boost=2):
        for task in self.heap:
            task.wait_time += 1
            if task.wait_time >= aging_threshold:
                task.priority += boost
                task.wait_time = 0
        for i in range(len(self.heap) // 2 - 1, -1, -1):
            self._max_heapify(i)

    def is_empty(self):
        return len(self.heap) == 0

def simulate_scheduler():
    scheduler = MaxHeapPriorityQueue()
    tasks_batch = [
        Task(1, "Background_Backup", 2),
        Task(2, "Antivirus_Scan", 4),
        Task(3, "UI_Render", 9),
        Task(4, "Audio_Stream", 8),
        Task(5, "Log_Collector", 1),
        Task(6, "Network_Sync", 5)
    ]

    print(">>> Enqueueing Initial Tasks into Max-Heap:")
    for t in tasks_batch:
        scheduler.insert(t)
        print(f"  Inserted: {t}")

    print("\n>>> Scheduler Simulation Starts:")
    clock = 1
    while not scheduler.is_empty():
        current = scheduler.extract_max()
        print(f"[Clock Cycle {clock}] EXECUTED -> {current}")
        scheduler.apply_aging()
        
        if clock == 2:
            urgent_task = Task(99, "KERNEL_INTERRUPT", 10)
            print(f"  [!] Alert: Urgent Task Arrived: {urgent_task}")
            scheduler.insert(urgent_task)
            
        clock += 1

if __name__ == "__main__":
    simulate_scheduler()
