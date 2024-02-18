
import json

class CommentCollection:
    def __init__(self):
        self.comments = []

    def add(self, comment):
        if comment not in self.comments:
            self.comments.append(comment)
        else:
            raise ValueError("Comment is already in the collection")

    def remove(self, comment):
        self.comments.remove(comment)

    def get(self):
        return self.comments

    def get_by_id(self, id):
        for comment in self.comments:
            if comment.id == id:
                return comment
        return None
    
    def clear(self):
        self.comments.clear()
    
    def to_dict(self):
        return [comment.__dict__ for comment in self.comments]
    
    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)