import base64
import json
import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

MagicKey = b"41100c93a65cfb71d5b0672c0d60d7ec"
MagicIv = b"70ba69d67bf7e61e17ac565c6093a325"[:16]


def Decode(data: bytes) -> bytes:
    cipher = Cipher(
        algorithms.AES(MagicKey), modes.CFB(MagicIv), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    return decryptor.update(data) + decryptor.finalize()


def get_version_name(version_code):
    version_names = {
        "basic": "个人商业版",
        "pro": "专业版",
        "ent": "企业版",
        "max": "豪华版",
        "ultra": "旗舰版",
    }

    return version_names.get(version_code, f"未知版本 ({version_code})")


def timestamp_to_datetime_string(timestamp):
    datetime_object = datetime.datetime.fromtimestamp(timestamp)
    datetime_string = datetime_object.strftime("%Y-%m-%d %H:%M:%S")
    return datetime_string


def main():
    print("许可证解码器 | GoEdge 分遗产版")
    print("本脚本无需输入申请码，免费开源。")
    print("开源仓库链接：https://github.com/GoEdge233/keygen-python")
    print("请按照提示输入信息：")

    encoded_data = input("请输入要解码的 Base64 编码数据: ")
    try:
        decoded_data = base64.b64decode(encoded_data)
        decrypted_data = Decode(decoded_data)
        json_data = json.loads(decrypted_data.decode())

        # 提取信息并格式化为人类可读形式
        human_readable_info = (
            f"用户 ID: {json_data.get('id')}\n"
            f"开始日期: {json_data.get('dayFrom')}\n"
            f"结束日期: {json_data.get('dayTo')}\n"
            f"生效时间：{timestamp_to_datetime_string(json_data.get('updatedAt'))}\n"
            f"公司/组织名: {json_data.get('company')}\n"
            f"可用节点数: {json_data.get('nodes')}\n"
            f"激活版本: {get_version_name(json_data.get('edition'))}\n"
            f"邮箱: {json_data.get('email')}\n"
        )

        print("\n解码后的信息:")
        print(human_readable_info)

        pretty_json = json.dumps(json_data, indent=4, ensure_ascii=False)
        print("解码后的 JSON 数据:")
        print(pretty_json)

        print("\n\n欢迎关注 GoEdge 分遗产频道 https://t.me/goedge233")
    except Exception as e:
        print(f"解码错误: {e}")


if __name__ == "__main__":
    main()
