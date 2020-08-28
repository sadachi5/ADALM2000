set(url "file:///home/debian/ADALM2000/cmake-3.8.2/Tests/CMakeTests/FileDownloadInput.png")
set(dir "/home/debian/ADALM2000/cmake-3.8.2/Tests/CMakeTests/downloads")

file(DOWNLOAD
  ${url}
  ${dir}/file3.png
  TIMEOUT 2
  STATUS status
  EXPECTED_HASH SHA1=5555555555555555555555555555555555555555
  )
