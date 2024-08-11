class Playlist():
    def __init__(self):
        self.queue = []
    
    def add_to_queue(self, user, song_title, video_url, audio_url):
        self.queue.append({
            'requested_by': user,
            'song_title': song_title,
            'video_url': video_url,
            'audio_url': audio_url
        })

    def remove_from_queue(self, index):
        self.queue.pop(index)

    def get_queue_length(self):
        return len(self.queue)
    
    def get_next_song(self):
        return self.queue[0]
    
    def get_queue(self):
        index = 1
        queue_str = ""
        for request in self.queue:
            if self.get_queue_length() < 1:
                queue_str += f'{index}. {request['song_title']} requested by {request['requested_by']}'
            else:
                queue_str += f'\n{index}. {request['song_title']} requested by {request['requested_by']}'
            index += 1
        
        return queue_str