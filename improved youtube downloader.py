from pytube import Playlist, YouTube
import os
import threading


def playlist_downloader(video_list, path='videos'):
    if not os.path.exists(path):
        os.mkdir(path)

    for video_url in video_list:
        try:
            v = YouTube(video_url)
            v.streams.first().download(path)
            print("Downloaded {}".format(v.title))
        except Exception as e:
            print(e)
            with open(os.path.join(path, "problems.txt"), "a") as f:
                f.write("Failed download: {}\n".format(e))
            continue


def split_array(array, n_groups):
    # splits an array into n groups
    split = []
    len_group = len(array) // n_groups
    remainder = len(array) % n_groups
    for i in range(n_groups):
        split.append(array[i*len_group:i*len_group + len_group])
    for i in range(remainder):
        split[i].append(array[-(i+1)])
    return split


def multi_thread_playlist_downloader(playlist_url, no_threads, path='videos'):
    pl = Playlist(playlist_url)
    pl.populate_video_urls()
    print("Fetched {} videos".format(len(pl.video_urls)))

    split_playlist = split_array(pl.video_urls, no_threads)
    threads = []
    for i in range(no_threads):
        thread_obj = threading.Thread(target=playlist_downloader,
                                     kwargs={
                                         'video_list': split_playlist[i],
                                         'path': path
                                     })
        threads.append(thread_obj)
        thread_obj.start()

    for thread in threads:
        thread.join()
    print("Complete")


url = r'https://www.youtube.com/watch?v=3S15Us4QuLs&list=UUsY94ljKzTlXNueC2m3hf-A'
multi_thread_playlist_downloader(url, 5)
