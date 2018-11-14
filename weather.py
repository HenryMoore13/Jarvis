import requests
import json
import math

secrets = json.load(open("secrets.json"))


class WeatherAPI:
    DEFAULT_ZIP = secrets['WeatherInfo']['ZIP_Code']
    URL_FORMAT = "http://api.openweathermap.org/data/2.5/weather?zip={zipcode},us&APPID=" + secrets[
        'WeatherInfo']['WeatherAPI_Key']

    def __init__(self, zipcode=None):
        self.zipcode = zipcode or self.DEFAULT_ZIP

    @property
    def url(self):
        return self.URL_FORMAT.format(zipcode=self.zipcode)

    def get(self):
        response = requests.get(self.url)
        data = response.json()
        return Weather(
            weather={
                'description': data['weather'][0]['description'].title(),
                'wind': data['wind']['speed'],
                'temp': data['main']['temp'],
                'weather_ID': data['weather'][0]['id'],
                'humidity': data['main']['humidity'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max']
            })


class Weather:
    def __init__(self, *, weather):
        self.weather = weather

    @property
    def temp_f(self):
        return kelvin_to_fahrenheit(self.weather['temp'])

    @property
    def min_temp_f(self):
        return kelvin_to_fahrenheit(self.weather['temp_min'])

    @property
    def max_temp_f(self):
        return kelvin_to_fahrenheit(self.weather['temp_max'])

    def get_image_URL(self):
        if 200 <= self.weather['weather_ID'] < 300:
            return "https://image.flaticon.com/icons/svg/1159/1159072.svg"
        elif 300 <= self.weather['weather_ID'] < 400:
            return "https://image.flaticon.com/icons/svg/1113/1113757.svg"
        elif 500 <= self.weather['weather_ID'] < 600:
            return "https://image.flaticon.com/icons/svg/1147/1147581.svg"
        elif 600 <= self.weather['weather_ID'] < 700:
            return "https://image.flaticon.com/icons/svg/1206/1206975.svg"
        elif 700 <= self.weather['weather_ID'] < 772:
            return "https://image.flaticon.com/icons/svg/577/577598.svg"
        elif 781 == self.weather['weather_ID']:
            return "https://image.flaticon.com/icons/svg/1167/1167621.svg"
        elif self.weather['weather_ID'] == 800:
            return "https://image.flaticon.com/icons/svg/1180/1180492.svg"
        elif 801 <= self.weather['weather_ID'] < 804:
            return "https://image.flaticon.com/icons/svg/861/861059.svg"
        elif self.weather['weather_ID'] == 804:
            return "https://image.flaticon.com/icons/svg/1200/1200405.svg"
        else:
            return "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxITEBISEhAQEBUVFRgVFRUPFRUVEhgVFREWFhUXFhYYHSggGB0lGxUVIjEhJSkrLi4uFx8zODMtNygtLisBCgoKDg0OGxAQGi0lHSUtLS0tLS0tLTctLi0tLS0tLTUtLy0tLS0tLS0tLS0tLS0rLS0tLS0tLS0tLS0tLS03Lf/AABEIAMsA+QMBIgACEQEDEQH/xAAcAAEAAQUBAQAAAAAAAAAAAAAABAECAwUGBwj/xAA9EAACAQIDBQUGBAUDBQEAAAAAAQIDEQQFIRIxQVFhBhMicZEHMoGhscFSYtHwFCNCcuGSorIzY3OC0hX/xAAaAQEAAwEBAQAAAAAAAAAAAAAAAQIDBAUG/8QALREAAgIBAwMCBQMFAAAAAAAAAAECEQMSITEEBUFRYRMiMnHwI6GxFDNCgZH/2gAMAwEAAhEDEQA/APcQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWzkkm3okc1m3aZRezTW0+r0Quh9jfYrFRgvFJL6msqZ5TT0lp1ZxeOxWIqP3tlPkQ55e2tZNszeVLg1WCT5PRaOe0n/AFI2dGspK6aZ5BHAST0k0+hu8Lm9WjFeLatzCyJkSwyR6QDQ5T2ijUttWV+K3G+NDMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA5ztlmDhBU4+9M5ShBQVt7e99TbdqZXxLfJWXoaZSOfLLejpwRVWSUiyuuSMkXp+/0KNX4L9/ApWx0WQ5yI9Wd1ZkjEv06GuxDaTe4qWZfl2McJbL1V/S56lkmJ26MXe7Wj+3yseN0qviv+956J2Ex99uk+Cuvuv3yOnG7RwZY1KzsAAaGYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABw/adLv3JNNN624NaO5yFXGVdpuEHJX0XTnc6fOaahiK0ODmpK/CUtXbzuzQY+NTdFuKSb00vZN2v13GMmpM6YRcUSMuxsp6TpunL1T/AEJlSqkm3w4HPYGrVaTtJav3r6pW113XvxJebVGqaavrqyjVbG0XasiYuvWqS0tFcFexErQqr33eNuGtiTLAy7uc9nbkoppO7vf8Oqu15mPA06jg1PS6uk3u5rUs1tZTa6I1HelzZvsszyGEqKTUpO+qjvsaCUXGV7aoj4ak6kqjb1Svr05EKelD4WuW/B7zleYQr0oVYX2ZLc96fFPqSznOwMbYKPWTfyS+x0ZvF2jmnFRk0gACSgAAAAAAAAAAAAAAAAAAAAAAAAAAAAABwvbCns4natvUZei2fsjSxk2rr43O27VZZOrCMqa2pReqVruL8+T+5xGLpSpVJQkrNb1vtdX+5zTTUrO/FJSikW1Itau1+RAzidtlct5ldZ6yab10t0IWdZgnZRi23a5Xk2pIl4OpJwTjLTc1y/wVqO0W+L3+RrMHWmpXtsp8OpIx9T99A/QUqIGKnq2i7LKcrt299OK9N5GndrTid12CyfvnCs0u6pt8U3KcXutyT1+CJUW9kZuSjcmdzkOC7nD0qb3qN5f3PVr52+BsADqSo89u3YAAIAAAAAAAAAAAAAAAAAAAAAAAAABSckk23ZLVt8gCpbOaSu2kub0R592j7eyu4Ya0UtNtq8n5J6I4fG5vVqt95UnO/wCKTa9NyMpZUuD1cHass1cnX8nttXOcNH3sTQXnUh+pxHabFUa1fbo1I1FspScd20vrpY8022na7Nx2dxdpuL3S3ea/w/kZyyOSo6Jdtjig5pttG5liIQspXfRJt/Isq1KbTbpyen4JX+hInRfvRtd/roY6lKpvc2nyS0JjwcVo09XFRbSSnHzi0jJjL92r89n6P7kh4PafP4fYxZnK0Y01+JNc3w9NCGgpK6NXmNVU436aefAhZHn2JopU6NepTim5tQdk5NJa89xCz/G7dRpPSOnx4mLK4Ozk+O7qOFZ6PT4U9muTt4ducao276T+Cv62Ise0+Mb2niq9+k2l6bjRxRkKan6noLp8S4iv+HQ0u2OMjr/EVJf36o6XIvaPqo4mKt+OG9dWuJ5vPc3yMUZExm0Y5ujwzVOKPpChWjOKnCSlGSumtU0zIeb+y3PtZYOpL89K/wAXOP39T0g6k7VnzWfE8U3FgAEmIAAAAAAAAAAAAAAAAAAOU9ouad1hdhO0qrt12Vq/sjqzxv2kYycsdOMt0LRiuFtlP6tlMjqJ3dvxfEzq/G5zNSWpjuXS95lkjlPq0VnG5i2mnya1VvsZLlkmno/UlENHTZJnicdiq7SXuyeia5Pk7m2rYuG7bhz0aOA3aPdwf6mGrSjf8LNUzyc3boylqi69jt8TjoKLe1frfqcbnGatytCV3uuuC6ESqlxm/K5i7rilsrm978kX8FMfRKEvUxYfD7Urev6G2Vr24IwUo7MdFa+7n5skUYmE3Z6mKCiZbFKkrFeJiqvVFDVjFStTbLVK1uLtuKZn/wBMso7k+hK4M5P569jPQxE6dSFWEnGcXdNcGndH0RlWNVahSqrdOClp1Wq9T5yqrTy1R617Is27zDToN60pXj/ZPX5Sv6m+Jni9zxbal4O+BQqbHigAAAAAAAAAAAAAAAAAA8M7d19rH1/77f6fD9j3M+fO09W+LrS/7s3/AL2ZZeD1u0r9ST9iLP3mUmKj8T8xM5j6RFiLpK5QrTLAxtNbtejMNRripL5olyiY9hlkykokLaX9MG31RdGm77U+G5EuTS3mGMXJ3e4lyK6RBXd2SI6IsjvL5szZolRWJHTvMzydkRsP7xBD5SK5m/DboY8G7wXkY8RLarW5Irl3uvo2vmW8GCd5L/NiQmb72d5p/D5hSu7RqPupcrVH4fSaRzyepSTaaknZp7+Wuj9bFoumY9TjU4NH00DX9n8w/iMLQrfjpxb6St4l8Hc2B1HyjVOmVAAAAAAAMWKjJwmou0nFqL5O2gBkuVPL8xqV6MrVITpvnrZ/+y0Zdlee1k5fzJJLSzlf5Mz1+qOn+ndWnZ6cDjIdoKrWk7vlaJLodppq3eU1LrF2LakZPFJHUAg5fmtKtpCXiSu4vSX+ScWM3sD5xzed61R/mf1PoutO0ZN6JJv0R82YyptTlLnJv1Zjl8Hsdo5k/sZp7/T6F0txY3ez6f4L76HOfQLgtQRRFWCTImY6ky5Mx7F2AzGoXepdUdtEX1JWRiprW5NkexlpRsUvqXPcWwIJKYh6GHCbymJqFcGPBT/Iixf8+XWNzJlr8L/ul9TBV0xHnB/UyYB6S/uZd8HPjfz/AO2ZmtWXNXVi+99DHudiDRrweveyDH7eDnSb1pVH/pmr/wDJT9TvDx72S4vYxsoX0q02rfmhZr5J/M9hOqDtHy3WY9GZoFShUscwAAAAIuNzCnSXjkl0WsvQCrJMop6NJ+Zrc0lh6cG6lOm+UdmO1J9EaPMO1rbcaSUF+Kdtr03I0axPeJzlJyu/ebvf/BRz9DeGFvdlKUEm5JbF22o3b2U9bfAzKpwIk0+F7fIvpLzMjqZjqOUZKUG4yWqcdGjZZX277qpGjjHpLSNayST5VLaW/MvjzI9rauyXNmoz2FOpBxkk1z/QaqK6FLZo7b2g5wqOAm4yV6q7uDTvdSV2102b69UeFtkvMcwquEMPUqSlGk5d2m9FwaXR2T6XZq6ddN23Mib1bnqdHjjhjpvnc2NL3V8fqzMtxgoS8K+P1MsTJ8nqR4BcWFyZBYqhKdkUZhmCGy3ezNBFsUX3JCLajOpyHIopKpWjtPfGD3LrLm+hA7PZU5SVWcXsLWN90n5ckdYp6NtN8ki8V5PL6zqt/hwf3ItfFwhL3YxXRJfA5jPnTdXagkm/eS3dH5kjP6kkpP3bX929t3FveczhK+03d3YlwZdCv1Lsh5i7VacurXqjLhP6vMw5q9V0kn8zPhOLD+k7of3H+eDOi6Ubq3HgyqZeilnRSZJ7OZk6OJpVdzhNNryevqrr4n0TTmpJSTumk01xTV0fMmJVntryf2Z7v7Os07/AUm3eVO9OXPw+7/tsdOJ+Dwe54+Jemx0wANTxyoABIPPe0VFxnPvJXad20991db+h6EYp4eDd3CLe67SbsVlGzTHk0OzyhYSKSqqFk1o5yb39HuLZYptq8qcFfxO9/hbQ9Gx3ZvDVU1KDV/wSkreS3HPLsBGnPbhU77lCqkvjtLfbyKODOhZ4M0kcxhKooLxdYrwr4mTFYyCf0JmK7H41t7E8Oly2pf8AybLKuwdKMb4mTrza3JtQi/y2s38SFBkvNBHC4/ONrw7Vl0325HP47O1tbFNbT+S6v9Cva3KquGxFSjUu4p+F2spQesX6GigrbkrdCGjrx4tVO9i7EzbldkWqyW1ci1I+8VR3vg2GV1Lwd+D+xNRqsnnrJc0mbO5Sa3OrBK4FWytywXKmxdJmMrJlECC+Jt+z2Xd7UvJeCGsur4RNQmd32cwqhh48HJbb53ktPlYmKObrMzx49uWbFzSSVtOCMU9Fctrzte2jXM0+PzdR00b6bjQ8I0XazFK0or4+pydOp4t9mTs8xynUevnbmamnLVstR14FpX3JrkpaS571v0JdK1rR4GtpmfvdNlFWjshOtyZK/CSXmjDHEVIvXZa9Cu3ZrqHK5WjVy9y+GNi3ZrpZnoHsjzLusVKhtXhXj4ek4Jys+T2drzsjzqcE1e11yJOS5jUwtenVg9rZkpRvuduDNI7HL1EXODi/J9OAhZNmUMRQp16fuzje3FPc0+qd0TTc+daadMqAAAAACjAAIBQFCSDXZ7k9LFUpU6kIyutG0tqL4NPgfP2e5LUw1aVKpGzW58GuDTPpI0fans3SxlJxmrSXuTW+L/ToVlGzr6XqfhOnwfPEXYsS1Zus8yGrhqjp1ItcnwavvTNT3epi0e1GadNcGLKlab6Jr5o2lzX4dbM7k180UnydPT/SVcim0NoJFDpRW4KFUQSbjL8hlVpqptxipS2Yre99m3yR1Nd7FP3leCsteStdnC0sbUgkozkkndJbrltXHVZb5t/Iumkef1GDLllyq8G6q53JQlFxWr0d7HL4/E1L+FqK8v3YkPq7mDEMaisehilcnb/Y0s48OPEzQhZa6EiUb8k+djC8PJ8bmlldGktbXAkUI8TCqDXAyEMmO25lxLvG/JltOW4VX4H8PqiykwlsTKXzEqjva5lq5P8AbL6S8SLXG8n5r6Bcib+U9v8AZE5f/nLa4VZpeWl/nc7U03Y/Lf4fBUKTVpbO1Jfmm9qX1t8DcnQlSPnsstU2/cqAAUABQAFCrKMkqygDKEkAoCgBFzHLqVeDhVpxnHk+HVPgzgM99mad5Yapb8lXd8JL7npJQhpPk1xZ54/pZ8+4zstjIVVB4aq5XVtiLlHz2loQZxcW4vem16Ox9Ho+d82X86r/AOWp/wA2YZIJI9rt/VSyyaaI2gLCtzA9dMrcXKFCCbLri5aCQVuR6xmMFQIpPgsjEjYklLcQ8YXjyc+XaJipYuXHxLrv9STCvB7nsv8ANp8yAtwfA0o41Jo2tSm9kwU1dGCjVkpxSbSe9cPQ3VShFbkKovq1EXDy1O49m3Zx4jF99KP8qk1J3WkpWezH1s/gcQ1qfQ/YrDQhgMOoRUbwUnbjJ6tstCO9nN1eZwx0vJvQEDU8c//Z"


def kelvin_to_fahrenheit(k):
    return math.floor((int(k) - 273.15) * (9 / 5) + 32)
