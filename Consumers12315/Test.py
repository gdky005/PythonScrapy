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


body = '''
    <span lang="EN-US" style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">1.</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312;color:black">当心掉进健身预付卡消费陷阱</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">预付款消费是指消费者预先向经营者交付一定额度的消费金额，按照事先的消费约定，以整存零取的方式接受商家的服务，一般会获得商家承诺的额外优惠。例如，一次性接受商家服务消费<span lang="EN-US">20</span>元，如果一次存入<span lang="EN-US">100</span>元，商家可以发给一个消费卡，并且可以享受<span lang="EN-US">6</span>至<span lang="EN-US">7</span>次的优惠服务，降低了正常消费金额，颇受消费者青睐。经营者一次性预收消费者现金相当于有了固定客源，因此预付款消费在很多服务行业颇为盛行。</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">近年来，由于经营者的经营方式方法及诚信经营理念不同，消费者的消费理念存在差异，以及贪图便宜心理的存在，预付款消费纠纷成为消费者投诉的热点。例如，某健身俱乐部办理会员消费卡涉及消费者<span lang="EN-US">100</span>多人，现在是人走楼空，中途停止营业，有的消费者已存消费卡金额达<span lang="EN-US">3000</span>余元，但找不到当事人，致使维权之路至今未果。</span>
<span style="font-size:16.0pt;font-family:仿宋_GB2312">消费者进行预付款消费应注意以下事项：第一，要多做比较。消费者应尽量选择规模大、信誉好、经营状况良好的企业，不轻信广告和商家的口头承诺，不受促销的诱惑。第二，要签订合同。消费者与经营者应当签订书面合同，应载明价格、服务标准、优惠条件、使用商品品牌、有效期限、有效次数、使用权限、使用地点、续费升级、遗失补办等事项，并应明确预付款消费卡的功能、使用范围、有效期限、退卡（款）条件、违约责任等事项。对以格式合同、通知、声明、店堂告示做出对消费者不公平、不合理的规定，“最终解释权归本经营者所有”等提示，免除其损害消费者合法权益、加重消费者责任或排除消费者权利的内容，要坚决说不。第三，要适度消费。在办理预付款消费卡时，首先要弄清自己是否真的长期需要此类服务，应根据自身实际需要购买、充值预付款消费卡，每次充值金额不宜过多，谨慎选择预付额度过高、服务周期过长的预付款消费。要按照自己的实际需求量来购买预付款消费卡，不要贪便宜一下子大量购买，以避免承担过多风险。第四，要慎重进行预付款消费。因为预付款消费目前还没有专门的法律规定，现在购物、金融、洗浴、洗车、游泳、健身、美容、餐饮、娱乐等行业出现预付款消费纠纷后，只能使用旁法为消费者维权，为此要提醒消费者慎重选择预付款消费，并要注意妥善保管好相关的服务章程、协议和票据等消费凭证。第五，要及时维权。消费者发现经营者的经营行为有异常时，要及时向有关部门咨询或举报，避免办卡容易退卡难现象发生。一旦经营者需要变更经营地址、注销或整体转让经营资质，或商品质量、商品价格、服务质量、服务价格发生变化时，经营者应提前告知消费者，协商是退费还是继续履行合同承诺，若协商不成消费者可请求所辖地消费者协会调解，也可向有关行政职能部门申诉。对经营者未尽告知义务又无法履行合同承诺的侵权行为，消费者可向所在地行政职能部门提出申诉或向人民法院提起诉讼，以维护自身的合法权益。</span>

'''


content = Selector(text=body).xpath('//body/span//text()').extract()

# <class 'list'>: ['并且可以享受', '6', '至', '7', '次的优惠服务']


space = "\r\n\n\t"

content1 = ""
for line in content:

    if Utils.matchTitle(line):
        # content1 += line
        content1 += space
        continue

    content1 += line
    endChar = line[len(line) - 1]

    if Utils.isEndChar(endChar):
        content1 += space

print(content1)











