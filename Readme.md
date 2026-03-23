# u8g2中文字型轉換python工具 (適用Arduino/ esp32等)


如果要用Arduino, esp32等mcu顯示中文，可以使用u8g2 library，本身就支援繁體中文。

但是繁體中文字符超多，u8g2內建的幾個中文字型都會有缺字。

u8g2有提供取字教學，也有幾個.bdf中文字型如/tools/font/bdf中的unicode和wenquanyi

但是手動取字太痛苦了，後來我在網上搜到Jeffrey大的這篇<a href="https://blog.darkthread.net/blog/u8g2-cht-font-tool/">powershell自動取字工具</a>

根據本人使用習慣改成python，得到Jeffrey大的同意在此分享，希望可以幫助大家

P.S. 本有只有用WINDOWS，不確定其他系統是不是可以用bdfconv，如果不能應該也可以生成的chinesemap.map另作下游處理?



## 用法:

1. 下載所需檔案: 
- 下載<a href="https://github.com/olikraus/u8g2/tree/master">u8g2 library</a>

- 下載本repo的 u8g2_convert.py

- 你可以將u8g2_convert.py放到library的tools/font中

- 或是將u8g2中的tools/font/bdfconv這個目錄放到u8g2_convert.py所在地



2. 預備好.bdf字體和一個你需要取字的文字檔



3. 使用範例:
```bash
python u8g2_convert.py -i 路徑/字體.bdf -s 路徑/取字.txt -n 字體名(請用英文數字)
```
會在字目錄converted_fonts/下生成: u8g2_font_<字體名>.c


4. 生成的 u8g2_font_<字體名>.c 可直接使用:

```bash
#include "路徑/u8g2_font_<字體名>.c"
u8g2.setFont(字體名); 
```

後面其他就是跟平常u8g2用法就行，u8g2的使用方法和bdf的轉換這篇就不說明了，網上相關的教學很多


## 效果:
<img width="600" src="https://github.com/user-attachments/assets/c1825f17-7bdf-42e5-9b85-6cd12746562c" />



(使用4.2寸三色墨水屏,這是我本人另一個repo: <a href="https://github.com/mahbird/Weather_Postcard">Weather Postcard</a> (香港用的天氣站) 正在施工中的中文化計劃，使用的是google的NotoSans字型，完成後中文版會上線，請多多支持




## Source and Credit:
- Coding4Fun – Arduino/ESP u8g2 中文字庫自動化工具 (https://blog.darkthread.net/blog/u8g2-cht-font-tool/)

- u8g2 by olikraus (https://github.com/olikraus/u8g2/tree/master)

- Developed with assistance from Microsoft Copilot




