import random
import string
import base64
import datetime
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from pydantic import BaseModel, Field, field_validator
from typing import List

MagicKey = b"41100c93a65cfb71d5b0672c0d60d7ec"
MagicIv = b"70ba69d67bf7e61e17ac565c6093a325"[:16]


def Encode(data: bytes) -> bytes:
    cipher = Cipher(
        algorithms.AES(MagicKey), modes.CFB(MagicIv), backend=default_backend()
    )
    encryptor = cipher.encryptor()
    return encryptor.update(data) + encryptor.finalize()


class KeyGen(BaseModel):
    id: str = Field(..., description="ID")
    dayFrom: str = Field(..., description="开始日期 (YYYY-MM-DD)")
    dayTo: str = Field(..., description="结束日期 (YYYY-MM-DD)")
    macAddresses: List[str] = Field(default_factory=list, description="MAC地址列表")
    requestCode: str = Field(..., description="请求码")
    hostname: str = Field("*", description="主机名")
    company: str = Field(..., description="公司/组织名")
    nodes: int = Field(0, description="节点数 (0为无限制)")
    updatedAt: int = Field(0, description="更新时间戳")
    components: List[str] = Field(default_factory=lambda: ["*"], description="组件列表")
    edition: str = Field("ultra", description="版本 (basic/pro/ent/max/ultra)")
    email: str = Field(..., description="邮箱地址，可选")

    @field_validator("edition")
    def check_edition(cls, v):
        if v not in ["basic", "pro", "ent", "max", "ultra"]:
            raise ValueError("版本错误，必须在 basic/pro/ent/max/ultra 中选择")
        return v

    @field_validator("dayFrom", "dayTo")
    def check_date_format(cls, v):
        from datetime import datetime

        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("日期格式应为 YYYY-MM-DD")
        return v


def generate_random_string(length=8):
    letters = string.ascii_letters
    return "".join(random.choice(letters) for _ in range(length))


def get_user_input(prompt: str, default: str = "") -> str:
    user_input = input(prompt + f" [{default}]: ")
    return user_input if user_input else default


def main():
    print("激活码生成器 | GoEdge 分遗产版")
    print("本脚本无需输入申请码，免费开源。")
    print("开源仓库链接：https://github.com/GoEdge233/keygen-python")
    print("请按照提示输入信息：")
    data = {
        "id": generate_random_string(),
        "dayFrom": get_user_input("请输入开始日期 (YYYY-MM-DD)", "2000-01-01"),
        "dayTo": get_user_input("请输入结束日期 (YYYY-MM-DD)", "2999-12-31"),
        "macAddresses": [],
        "requestCode": "*",
        "hostname": "*",
        "company": get_user_input("请输入公司/组织名", "@goedge233 | Goedge 分遗产版"),
        "nodes": int(get_user_input("请输入节点数 (0为无限制)", "0")),
        "updatedAt": get_user_input("请输入更新时间戳 (int)，默认为当前时间", int(datetime.datetime.now().timestamp())),
        "components": ["*"],
        "edition": get_user_input(
            # basic: 个人商业版
            # pro: 专业版
            # ent: 企业版
            # max: 豪华版
            # ultra: 旗舰版
            "请输入版本 (basic/pro/ent/max/ultra) (默认 ultra): ",
            "ultra",
        ),
        "email": generate_random_string(4) + ".goedge233@t.me",
    }

    try:
        keygen = KeyGen(**data)
    except Exception as e:
        print(f"输入错误: {e}")
        return

    encoded = Encode(keygen.model_dump_json().encode())
    print("\n\n激活码：")
    print(base64.b64encode(encoded).decode())
    print("\n\n欢迎关注 GoEdge 分遗产频道 https://t.me/goedge233")


if __name__ == "__main__":
    main()
