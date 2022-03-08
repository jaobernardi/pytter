class Tweet:
    def __init__(self, data) -> None:
        self.__dict__.update(data)
        # Placeholder
    
    def __repr__(self) -> str:
        return f"<Tweet id={self.data['id']}>"