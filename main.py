# importing the module
import pytube


url = 'https://www.youtube.com/watch?v=f6YDKF0LVWw'

youtube = pytube.YouTube(url)
video = youtube.streams.first()
video = youtube.streams.get_highest_resolution()
video.download('C:\\Users\lemba\PycharmProjects\ProyectoComputacion')
