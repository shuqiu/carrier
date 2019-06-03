import requests
import time
import cv2
from os import listdir
import os
from PIL import Image


class AlphanumV1(object):

    def __init__(self):
        self.k = 4

    # 获取验证码素材
    def get_pic(self):
        url = "https://login.189.cn/web/captcha?undefined&source=login&width=100&height=37"
        for i in range(100):
            img = requests.get(url).content
            with open(".//images//%s.jpg" % str(i), 'wb') as f:
                f.write(img)

    # 去除噪声图片
    def remove_picture(self, image):
        height, width = image.shape
        # 取图片的四个角的像素点，如果黑色像素点个数大于等于4个，认为是噪声图片
        corner_list = [image[0, 0] < 127, image[height - 1, 0] < 127, image[0, width - 1] < 127, image[height - 1, width - 1] < 127]
        if sum(corner_list) >= 3:
            return False
        else:
            return True

    # 分割图片
    def split_img(self, imagepath):
        # 以灰度模式读取图片
        img_gray = cv2.imread(imagepath, 0)
        # 将图片的边缘变为白色
        height, width = img_gray.shape
        for i in range(width):
            img_gray[0, i] = 255
            img_gray[height - 1, i] = 255
        for j in range(height):
            img_gray[j, 0] = 255
            img_gray[j, width - 1] = 255

        # 中值滤波
        blur = cv2.medianBlur(img_gray, 3)  # 模板大小3*3
        # 二值化
        ret, thresh1 = cv2.threshold(blur, 230, 255, cv2.THRESH_BINARY)

        # cv2.imshow('im',thresh1)
        # cv2.waitKey(0)

        # 最小外接矩形函数来提取单个字符
        image, contours, hierarchy = cv2.findContours(thresh1, 2, 2)

        char_imgs = []
        for cnt in contours:
            # 最小的外接矩形
            x, y, w, h = cv2.boundingRect(cnt)

            # 长宽都小于20，认为是噪声图片，去除
            if (w < 20 and h < 20) or (x == 0 and y == 0):
                continue
            # 宽度大于70的，存在干扰线干扰线
            elif w > 70:
                self.ganraoxian(imagepath)
            else:
                char_img = thresh1[y:y + h, x:x + w]
                if self.remove_picture(char_img):
                    char_imgs.append(char_img)

        # 如果获取的图片>5,第一张图片肯定是噪声图片，删除之
        if len(char_imgs) >= 5:
            char_imgs = char_imgs[1:]

        if len(char_imgs) > 0:
            for i in range(len(char_imgs)):
                cv2.imwrite('./cut/char%s' % (str(i) + '_' + imagepath.split('/')[-1]), char_imgs[i])
            os.remove(imagepath)

    # 根据颜色占比率，去除干扰线
    def ganraoxian(self, imagepath):
        print('k:', self.k)
        if self.k < 3 or self.k > 7: return None
        img = Image.open(imagepath)  # 读入图片
        width = img.size[0]
        heigth = img.size[1]  # 获取长宽
        smap = {}
        keylist = []
        for i in range(0, width):
            for j in range(0, heigth):
                argb = img.getpixel((i, j))
                r = argb[0]
                g = argb[1]
                b = argb[2]
                sum = r + g + b  # 得到每一点的rgb

                if sum not in smap.keys():  # 如果没有该sum值的点  进行添加  并且给值为1
                    smap[sum] = 1
                else:
                    num = smap[sum]
                    smap[sum] = num + 1  # 如果有了这个值  在原基础上+1
        slist = sorted(smap.items(), key=lambda x: x[1], reverse=False)

        if len(slist) > 4:
            # 得到颜色占比率最多的像素
            keylist.append(slist[len(slist) - 5][0])
            keylist.append(slist[len(slist) - 4][0])
            keylist.append(slist[len(slist) - 3][0])
            keylist.append(slist[len(slist) - 2][0])

        for x in range(0, width):
            for y in range(0, heigth):
                argb = img.getpixel((x, y))
                r = argb[0]
                g = argb[1]
                b = argb[2]
                ssum = r + g + b
                flag = True
                argblist = []
                for i in range(1, 4):  # px+1
                    if y + i < heigth and y - i > 0 and x - i > 0 and x + i < width:
                        upargb = self.get_pix(img, x, y - i)  # 上
                        endargb = self.get_pix(img, x, y + i)  # 下
                        rightupargb = self.get_pix(img, x + i, y + i)  # 右上
                        leftupargb = self.get_pix(img, x - i, y + i)  # 左上
                        leftdownargb = self.get_pix(img, x - i, y - i)  # 左下
                        rightdownargb = self.get_pix(img, x + i, y - i)  # 右下
                        leftargb = self.get_pix(img, x - i, y)  # 左
                        rightargb = self.get_pix(img, x + i, y)  # 右

                        argblist.append(upargb)
                        argblist.append(endargb)
                        argblist.append(rightupargb)
                        argblist.append(leftupargb)
                        argblist.append(leftdownargb)
                        argblist.append(rightdownargb)
                        argblist.append(leftargb)
                        argblist.append(rightargb)

                # 获取的附近的像素点，任意一个都在四个像素之一，就认为是验证码的线条
                if any(argbkey in keylist for argbkey in argblist):
                    flag = False
                # 中心像素点 和 其周围的像素点 不是四个像素点之一，就认为是干扰线的线条，设置为白色
                if ssum not in keylist and flag:
                    img.putpixel((x, y), (255, 255, 255))

        new_name = "grx_" + imagepath.split("/")[-1]
        new_imagepath = imagepath.replace(imagepath.split("/")[-1], new_name).replace(('jpg'), 'png')
        img.save(new_imagepath)
        if self.split_gex_img(imagepath, new_imagepath) is False:
            self.ganraoxian(imagepath)

    def split_gex_img(self, imagepath, new_imagepath):
        img_gray = cv2.imread(new_imagepath, 0)
        # 将图片的边缘变为白色
        height, width = img_gray.shape
        for i in range(width):
            img_gray[0, i] = 255
            img_gray[height - 1, i] = 255
        for j in range(height):
            img_gray[j, 0] = 255
            img_gray[j, width - 1] = 255

        # 中值滤波
        blur = cv2.medianBlur(img_gray, 3)  # 模板大小3*3
        # 二值化
        ret, thresh1 = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY)

        # 最小外接矩形函数来提取单个字符
        image, contours, hierarchy = cv2.findContours(thresh1, 2, 2)

        char_imgs = []
        for cnt in contours:
            # 最小的外接矩形
            x, y, w, h = cv2.boundingRect(cnt)

            # 长宽都小于20，认为是噪声图片，去除
            if (w < 20 and h < 20) or (x == 0 and y == 0):
                continue
            # 宽度大于70的，存在干扰线
            elif w > 70:
                self.k -= 1
                return False
            else:
                char_img = thresh1[y:y + h, x:x + w]
                if self.remove_picture(char_img):
                    char_imgs.append(char_img)

        print(len(char_imgs))

        # 如果获取的图片是四张，说明切片成功，读写图片，并移出原图素材
        if len(char_imgs) > 4:
            for i in range(len(char_imgs)):
                cv2.imwrite('./cut/char%s' % (str(i) + '_' + imagepath.split('/')[-1]), char_imgs[i])
            os.remove(new_imagepath)
            os.remove(imagepath)
            return True
        elif len(char_imgs) > 4:
            self.k += 1
            return False
        else:
            self.k -= 1
            return False

    def get_pix(self, img, x, y):
        rgb = img.getpixel((x, y))
        r = rgb[0]
        g = rgb[1]
        b = rgb[2]
        sum = r + g + b
        return sum


if __name__ == '__main__':
    c = AlphanumV1()
    c.get_pic()
    dir = "./images"
    for file in os.listdir(dir):
        imagepath = dir + '/' + file
        c.split_img(imagepath)
