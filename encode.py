import random
import string
import base64
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
    edition: str = Field("ultra", description="版本 (basic/pro/ent/sub/ultra)")
    email: str = Field(..., description="邮箱地址，可选")

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
    data = {
        "id": generate_random_string(),
        "dayFrom": get_user_input("请输入开始日期 (YYYY-MM-DD)", "2000-01-01"),
        "dayTo": get_user_input("请输入结束日期 (YYYY-MM-DD)", "2999-12-31"),
        "macAddresses": [],
        "requestCode": "*",
        "hostname": "*",
        "company": get_user_input("请输入公司/组织名", "@goedge233 | Goedge 分遗产版"),
        "nodes": int(get_user_input("请输入节点数 (0为无限制)", "0")),
        "updatedAt": 0,
        "components": ["*"],
        "edition": get_user_input(
            "请输入版本 (basic/pro/ent/sub/ultra) (默认 ultra): ", "ultra"
        ),
        "email": "goedge233@t.me",
    }

    try:
        keygen = KeyGen(**data)
    except Exception as e:
        print(f"输入错误: {e}")
        return

    encoded = Encode(keygen.model_dump_json().encode())
    print(base64.b64encode(encoded).decode())
    print("\n\n欢迎关注 GoEdge 分遗产频道 https://t.me/goedge233")


if __name__ == "__main__":
    main()
