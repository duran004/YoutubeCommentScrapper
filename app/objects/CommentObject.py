


class CommentObject:
    def __init__(self, comment : str, writer : str, comment_time : str, negative_point: float = 0):
        self.comment = comment
        self.writer = writer
        self.comment_time = comment_time
        self.negative_point = negative_point
        self.is_valid()
    
    def is_valid(self):
        if self.comment and self.writer and self.comment_time:
            return True
        raise ValueError("CommentObject is not valid")