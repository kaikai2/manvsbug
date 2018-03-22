import os
import enum
import random

class Status(enum.IntEnum):
    OPEN = 0
    CLOSED = 1
    INPROGRESS = 2
    
class Priority(enum.IntEnum):
    Blocker = 0
    Critical = 1
    Major = 2
    Normal = 3
    Minor = 4
    Trivial = 5
    
    def shift(p, r):
        p = p + r
        if p < Priority.Blocker:
            p = Priority.Blocker
        if p > Priority.Trivial:
            p = Priority.Trivial
        return p
    def name(p):
        return ["Blocker", "Critical", "Major", "Normal", "Minor", "Trivial"][Priority.shift(p, 0)]

class Issue:
    def __init__(self, id, priority):
        self.id = id
        self.status = Status.OPEN
        self.priority = priority

    def solve(self, solution):
        self.status = Status.CLOSED
        return random.randint(0, 3)

    def touch(self, id, seed):
        self.status = random.randint(Status.OPEN, Status.INPROGRESS)
        self.priority = Priority.shift(self.priority, random.randint(-2, 2))
        
class Project:
    def __init__(self, name, features, seed):
        self.name = name;
        self.issues = {}
        self.nextId = 1
        self.newIssues(features, seed)

    def issueName(self, id):
        return "{}-{}".format(self.name, id)

    def newIssue(self, priority):
        self.issues[self.issueName(self.nextId)]  = Issue(self.nextId, priority)
        self.nextId = self.nextId + 1

    def newIssues(self, n, seed):
        random.seed(a=seed)
        for i in range(n):
            self.newIssue(Priority.shift(Priority.Normal, random.randint(-3, 3)))

    def solve(self, issueId, solution):
        issue = self.issues.get(issueId, None)
        if issue:
            n = issue.solve(solution)
            causedIssue = 0
            for i in range(n):
                r = random.randint(1,2)
                if r == 1:
                    id = random.randint(1, self.nextId - 1)
                    touchedIssue = self.issues.get(id, None)
                    if touchedIssue:
                        touchedIssue.touch(issueId, solution)
                elif r == 2:
                    causedIssue = causedIssue + 1
            self.newIssues(causedIssue, solution)

    def summary(self):
        count = {}
        for issue in self.issues.values():
            if issue.status != Status.CLOSED:
                count[issue.priority] = count.get(issue.priority, 0) + 1
        return count
            
    def todo(self, priority):
        return {issue for issue in self.issues.values() if issue.status != Status.CLOSED and issue.priority <= priority}

def main():
    p = Project("LIME", 3, 1)

    while True:
        count = p.summary()
        for priority in sorted(count.keys()):
            print(Priority.name(priority), count[priority])

        print("TODO:")
        for i in p.todo(Priority.Trivial):
            print(p.issueName(i.id), Priority.name(i.priority))
        issue = input("Choose an issue:")
        p.solve(p.issueName(issue), 'normal')

        if len(p.todo(Priority.Normal)) == 0:
            print("You win")
            break

main()
