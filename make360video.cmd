rem c:\work\ffmpeg\ffmpeg -r 24 -start_number 1 -i "output/frame%%d.png" -vf "v360=c3x2:e" -c:v ffv1 -pix_fmt yuv420p equirectangular.mkv
c:\work\ffmpeg\ffmpeg -r 24 -start_number 1 -i "output/frame%%d.png" -vf "v360=c3x2:e" -c:v libx264 -crf 18 -pix_fmt yuv420p equirectangular.mp4
rem ffmpeg -r 24  -start_number 1 -i "output/frame%%d.png" -c:v libx264 -r 24 -pix_fmt yuv420p  output.mp4
