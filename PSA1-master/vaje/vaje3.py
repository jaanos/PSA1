# -*- coding: utf-8 -*-
class StackRecord:
    """Vnos v skladu"""
    def __init__(self, x = None, next = None):
        """
        Inicializacija vnosa v skladu.
        Časovna zahtevnost: O(1)
        """
        self.x = x
        self.next = next

    def __repr__(self):
        """
        Znakovna predstavitev vnosa v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.next is None:
            return "|]"
        return "|%s|<" % repr(self.x)

class Stack:
    """Sklad (LIFO)"""
    def __init__(self):
        """
        Inicializacija sklada.
        Časovna zahtevnost: O(1)
        """
        self.clear()

    def __len__(self):
        """
        Velikost sklada.
        Časovna zahtevnost: O(1)
        """
        return self.len

    def __repr__(self):
        """
        Znakovna predstavitev sklada.
        Časovna zahtevnost: O(n)
        """
        if self.len == 0:
            return "<|]"
        cur = self.top
        out = "<| %s" % repr(cur.x)
        cur = cur.next
        while cur.next is not None:
            out += " <- %s" % repr(cur.x)
            cur = cur.next
        return "%s |]" % out

    def clear(self):
        """
        Izprazni sklad.
        Časovna zahtevnost: O(1)
        """
        self.top = StackRecord()
        self.len = 0

    def peek(self):
        """
        Vrni vrhnji element v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.top.next is None:
            raise IndexError('peek on an empty stack')
        return self.top.x

    def pop(self):
        """
        Odstrani in vrni vrhnji element v skladu.
        Časovna zahtevnost: O(1)
        """
        if self.top.next is None:
            raise IndexError('pop from an empty stack')
        top = self.top
        self.top = top.next
        self.len -= 1
        return top.x

    def push(self, x):
        """
        Dodaj element na vrh sklada.
        Časovna zahtevnost: O(1)
        """
        self.top = StackRecord(x, self.top)
        self.len += 1

class QueueRecord:
    """Vnos v vrsti"""
    def __init__(self, x = None, prev = None, next = None):
        """
        Inicializacija vnosa v vrsti.
        Časovna zahtevnost: O(1)
        """
        self.x = x
        if prev is not None and next is None:
            next = prev.next
        elif prev is None and next is not None:
            prev = next.prev
        if prev is not None:
            prev.next = self
        if next is not None:
            next.prev = self
        self.prev = prev
        self.next = next

    def __repr__(self):
        """
        Znakovna predstavitev vnosa v vrsti.
        Časovna zahtevnost: O(1)
        """
        if self.prev is None:
            return ">|"
        if self.next is None:
            return "|>"
        return ">|%s|>" % repr(self.x)

class Queue:
    """Vrsta (FIFO)"""
    def __init__(self):
        """
        Inicializacija vrste.
        Časovna zahtevnost: O(1)
        """
        self.start = QueueRecord()
        self.end = QueueRecord(prev = self.start)
        self.len = 0

    def __len__(self):
        """
        Dolžina vrste.
        Časovna zahtevnost: O(1)
        """
        return self.len

    def __repr__(self):
        """
        Znakovna predstavitev vrste.
        Časovna zahtevnost: O(n)
        """
        if self.len == 0:
            return ">|>"
        cur = self.start.next
        out = ">| %s" % repr(cur.x)
        cur = cur.next
        while cur.next is not None:
            out += " -> %s" % repr(cur.x)
            cur = cur.next
        return "%s |>" % out

    def clear(self):
        """
        Izprazni vrsto.
        Časovna zahtevnost: O(1)
        """
        self.start.next = self.end
        self.end.prev = self.start
        self.len = 0

    def dequeue(self):
        """
        Odstrani in vrni prednji element vrste.
        Časovna zahtevnost: O(1)
        """
        last = self.end.prev
        if last.prev is None:
            raise IndexError('dequeue from an empty queue')
        self.end.prev = last.prev
        last.prev.next = self.end
        self.len -= 1
        return last.x

    def enqueue(self, x):
        """
        Dodaj element na konec vrste.
        Časovna zahtevnost: O(1)
        """
        QueueRecord(x, prev = self.start)
        self.len += 1

    def peek(self):
        """
        Vrni prednji element vrste.
        Časovna zahtevnost: O(1)
        """
        last = self.end.prev
        if last.prev is None:
            raise IndexError('peek on an empty queue')
        return last.x
