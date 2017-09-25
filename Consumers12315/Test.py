import re

from scrapy import Selector

from Consumers12315 import Utils

# # text = "1234['了文件']老人家了范德萨老家放"
# text = "['健身服务\n                    \n                ']"
#
# start = "['"
# end = "\n"
#
# print(text.find(start))
# print((end).__len__())
# print(text.find(end))
#
#
# print(Utils.sliptStr(text, start, end))


# text = "1.fafsasw1.fksafja;"
# print(Utils.matchTitle(text))



# line = "为是谁！"
# print(Utils.isEndChar(line))
# print(endChar)

# body = '<html><body><span>并且可以享受<span lang="EN-US">6</span>至<span lang="EN-US">7</span>次的优惠服务</span></body></html>'

# content = Selector(text=body).xpath('//body/span//text()').extract()


# # <class 'list'>: ['并且可以享受', '6', '至', '7', '次的优惠服务']
#
#
# space = "\r\n\n\t"
#
# content1 = ""
# for line in content:
#
#     if Utils.matchTitle(line):
#         # content1 += line
#         content1 += space
#         continue
#
#     content1 += line
#     endChar = line[len(line) - 1]
#
#     if Utils.isEndChar(endChar):
#         content1 += space
#
# print(content1)


body = '''
<p class="MsoNormal"><span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">44.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">冬季滑雪应注意什么？</span></p>
<p class="MsoNormal"><span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">&nbsp;&nbsp;&nbsp;</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">户外滑雪是一项具有高风险的运动项目，
由于能给滑雪爱好者带来速度与激情的愉悦感受，近年来喜爱滑雪的人越来越多。然而，由于一些滑雪场因场地设施隐患多、安全警示不到位，加之部分
滑雪者自我防护意识差，每年都有不少滑雪者在冰雪运动中发生意外，轻者肌肉拉伤、骨折，重者致残甚至死亡。目前正值滑雪旺季，
尤其在元旦、春节长假期间，许多人都会借机亲近大自然，选择冰雪运动。那么，冬季滑雪应注意什么？</span></p>
<p class="MsoNormal" style="text-indent:40.0pt"><span style="font-size:16.0pt;font-family:仿宋_GB2312">第一、备齐装备，注意保暖。
在做冰雪运动前，一定要备足御寒衣物，应尽量穿戴专业滑雪服、手套、滑雪帽。由于雪地上阳光反射较强，为避免雪盲，需要配戴专业滑雪镜。
在运动过程中，可根据身体发热程度适当减少衣物，提高人体舒适度。在运动结束后，要尽快到室内封闭场所，避免遭受风寒。</span></p>
<p class="MsoNormal" style="text-indent:32.0pt">
<span style="font-size:16.0pt;font-family:仿宋_GB2312">第二、享受冰雪，热身先行。冰雪运动较为激烈，一定要提前做好热身，
尤其要活动好髋、膝、踝、腕等各处关节和韧带。热身后能增加关节及韧带的柔韧性和活动范围，做好准备活动后再
滑，一般不容易摔倒，即使摔倒后受伤程度也会有所减轻。</span></p><p class="MsoNormal" style="text-indent:40.0pt">
<span style="font-size:16.0pt;font-family:仿宋_GB2312">第三、循序渐进，量力而为。要根据自身条件，选择相应难度等级的运动场地。
初学者应在教练陪同指导下练习，要在掌握必要的动作要领后再尝试单独滑行。即使有滑雪基础的滑雪者，也要先从初级道开始练习，逐步升级到高级道。
</span></p><p class="MsoNormal" style="text-indent:40.0pt">
<span style="font-size:16.0pt;font-family:仿宋_GB2312">第四、把握细节，安全第一。参加冰雪运动难保不发生摔倒情况，
因此要穿着安全防护设备，衣服口袋内要避免放置尖锐、易碎及硬质物品，以防摔倒过程中造成扎伤或顶伤。当身体将要失去平衡时，要立即通过弯曲身体、
收拢四肢等方式迅速降低重心，同时密切关注周边情形，以免相撞受伤或摔伤。一旦严重摔伤，身体感到剧烈疼痛，不要立即起身走动，应就近呼救求援，
必要时应拨打急救电话，寻求专业救助。</span></p><p class="MsoNormal" style="text-indent:40.0pt">
<span style="font-size:16.0pt;font-family:仿宋_GB2312">第五、避免风险，提早防范。滑雪是一项刺激性强的高
风险运动项目，凡患有心脏病、高血压、恐高症等疾病的人不宜参加。一般滑雪者在滑雪前要提早做好功课，对场地基础设施、安全防护措施、专业救护救援
等情况做到心中有数。同时，还要详细了解相关服务内容和注意事项，必要时主动购买意外伤害保险，确保万一受到意外伤害后，能减轻额外的经济负担。</span></p>
<p class="MsoNormal"><span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">45.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">游泳后易得哪些常见病？</span></p>
<p class="MsoNormal" style="text-indent:32.0pt"><span style="font-size:16.0pt;font-family:仿宋_GB2312">在炎热的夏天，
去游泳池游泳已成为很多市民选择的纳凉方式之一。可您知道吗？游泳后有<span lang="EN-US">5</span>种疾病容易发生。</span></p>
<p class="MsoNormal" style="text-indent:32.0pt">
<span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">1.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">咽结膜热。该病是上呼吸道感染的一个特殊类型，也叫“<span lang="EN-US">apc</span>热”，
由病毒感染引起。腺病毒存在于患者的呼吸道分泌物中，通过咳嗽、打喷嚏而散播在空气中，再经呼吸进入健康儿童的呼吸道。也可通过手、毛巾等为媒介，
从眼结膜侵入人体而导致发病，在夏季可通过游泳传播。咽结膜热是一种表现为急性滤泡性结膜炎，
并伴有上呼吸道感染和发热的病毒性结膜炎。该病多见于<span lang="EN-US">4</span>至<span lang="EN-US">9</span>岁儿童， 
早期症状为全身乏力，体温上升至<span lang="EN-US">38.3</span>℃至<span lang="EN-US">40</span>℃，伴有流泪、眼红和咽痛。
体征为眼部滤泡性结膜炎、一过性浅层点状角膜炎及角膜上皮下浑浊，耳前淋巴结肿大，多在<span lang="EN-US">5</span>至
<span lang="EN-US">6</span>天内痊愈。如果儿童游泳后几天出现发热等情况，要注意罹患咽结膜热的可能性。</span></p>
<p class="MsoNormal" style="text-indent:32.0pt"><span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">
2.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">急性出血性结膜炎。这是一种传染性极高的急性流行性眼病，俗称“红眼病”。其病原体可由多种病毒和细菌引起，
病原体通过被污染的手、毛巾、眼睛、脸盆、游泳池水等接触眼部间接传播。该病传染性极强，传播快，易在学校、工厂、幼儿园等人群聚集的地方爆发流行。
游泳池、浴池、理发店等公共场所往往是爆发流行的场所。
患者主要临床表现为有异物感、眼痛、流泪、畏光，以及水样分泌物增多，少数患者可能有全身发热、乏力、咽痛及肌肉酸痛等症状。</span></p>
<p class="MsoNormal" style="text-indent:32.0pt">
<span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">3.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">急性化脓性中耳炎。急性化脓性中耳炎是由细菌感染的中耳黏膜化脓性炎症，常因游泳而发病。
其主要症状为耳痛、听力减退及耳鸣，鼓膜穿透后出现流脓及畏寒、发热、倦怠等全身症状。</span></p><p class="MsoNormal" style="text-indent:32.0pt">
<span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">
4.</span><span style="font-size:16.0pt;font-family:仿宋_GB2312">沙眼。沙眼是由沙眼衣原体感染结合膜引起的一种慢性传染性结膜角膜炎。
急性发作期时有异物感、眼红、眼痛、流泪及产生黏液浓性分泌物，伴耳前淋巴结肿大。</span></p>
<p class="MsoNormal" style="text-indent:32.0pt">
<span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312">5</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">、日光性皮炎。这是一种与日光照射有关的光敏性皮肤病，在日光照射后几小时或几天发生瘙痒性皮疹，易发部位主要在颈下“
<span lang="EN-US">V</span>”区、手背、上肢以及小腿，停止日光照射后<span lang="EN-US">1</span>至
<span lang="EN-US">6</span>天或更久后可完全消退，愈后不留疤痕。</span></p>

'''

body1 = '''
<p class="MsoNormal"><span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">6.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">冬季游泳要注意什么？</span></p>
<p class="MsoNormal" style="text-indent:32.0pt"><span style="font-size:16.0pt;font-family:仿宋_GB2312">
很多人对游泳存在误区，认为游泳是夏天的运动，每当冬季来临，由于恐惧寒冷，就远离泳池了。事实上，因为气温低，冬天许多运动项目都容易造成
身体劳损或损伤，而游泳由于水的特殊环境能够将劳损和损伤降到最低。此外，冬天游泳，水温对人体皮肤表面形成刺激，能更好地促进血液循环。可见，游
泳不仅是一项适合四季的运动，更是一项需要长期坚持的运动。</span></p><p class="MsoNormal" style="text-indent:32.0pt">
<span style="font-size:16.0pt;font-family:仿宋_GB2312">室外寒风刺骨，游泳馆内温暖如春，室内游泳的确是一种享受。不过需要注意以下事项：
第一，装备要齐全。除泳衣、泳镜、泳帽等装备外，在冬天游泳一定要带拖鞋，以免脚底着凉；带浴巾或毛巾衣，以便在中间休息或沐浴后保暖。另外，游泳馆内温度高、
湿度大，建议身着相对简单、易穿脱且保暖性好的衣服，以便更衣。第二，准备活动要充足。与夏季相比，做好游泳前的准备活动更为重要。冬天由于气温低，关节相对脆弱，
下水前，一定要把各个关节活动开，应多做向上纵跳、拉肩、振臂等伸展运动，重点热身腿、臂、腰，以防游泳过程中发生抽筋。一般来说，准备活动时间大约为
<span lang="EN-US">5</span>至<span lang="EN-US">10</span>分钟，以感到身体微微发红、发热为好。第三，起水后要注意保暖。很多游泳者在游泳间隙休息
或上卫生间时不注意保暖，造成体温快速下降，导致受凉感冒。人的头部最易散热，如果起水、淋浴后头发湿漉漉，很容易造成热量迅速散失。因此，在起水后要披上浴巾，
沐浴后应及时擦干头发，穿好衣服，有条件的最好用吹风机将头发吹干。第四，掌握适宜的运动量。游泳者应根据年龄、性别、健康情况、运动基础、体力特点及运动习惯合
理制定健身计划，且持之以恒，一定能达到最佳的锻炼效果。</span></p>
'''

content = Selector(text=body).xpath('//p[@class="MsoNormal"]/span//text()').extract()

content1 = ""
isTitle = False
space = "\r\n\n\t"
space1 = "\r\n"

currentNumber = 0

i = 0

for line in content:

    if isTitle:
        content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space1
        content1 += "当前的问题是：" + line + space1
        content1 += "^^^^^^^^^^^^^^^^^^^^^^^^^^^^" + space

        isTitle = False
        continue

    if Utils.matchTitle(line):
        i += 1
        if i > 10:
            break

            # //把 line 转成成 数字存储起来
        lineNumber = int(line.split(".")[0])
        # print("下面是 lineNumber：")
        # print(lineNumber)

        if lineNumber < currentNumber:
            content1 += line
            continue

        currentNumber = lineNumber
        print("currentNumber:")
        print(currentNumber)

        content1 += "______________________" + space1
        content1 += line + "---------------" + space1
        content1 += "______________________" + space1

        isTitle = True
        continue

    if ~isTitle:
        l = line
        # for l in line:

        if Utils.matchTitle(l):
            # content1 += line
            content1 += space
            continue

        content1 += l
        text = l

        endChar = l[len(l) - 1]
        if Utils.isEndChar(endChar):
            content1 += space
print(content1)
