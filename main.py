import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import paramiko

class Watcher(FileSystemEventHandler):
    def on_created(self, event):
        print("File created")
        upload_to_sftp(
            hostname='your.sftp.server.com',
            port=22,
            username='your_username',
            password='your_password',
            local_filepath=event.src_path,
            remote_filepath='/path/on/sftp/to/upload/file.txt'
        )

        

def upload_to_sftp(hostname, port, username, password, local_filepath, remote_filepath):
    try:
        print("1")
        transport = paramiko.Transport((hostname, port))
        print("2")
        transport.connect(username=username, password=password)
        print("3")
        sftp = transport.open_sftp()
        print("4")
        sftp.put(local_filepath, remote_filepath)
        
        sftp.close()
        
        transport.close()

        print(f"File {local_filepath} uploaded to {remote_filepath}")

    except Exception as e:
        print(f"Error: {e}")



if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = Watcher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
