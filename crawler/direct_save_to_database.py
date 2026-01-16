import json
import os
import sys

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置DJANGO_SETTINGS_MODULE环境变量
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "soulStation.settings")

# 导入Django配置和模型
import django
django.setup()

# 导入模型
from api.models import PsychologicalKnowledge, PsychologicalKnowledgeDetail

# 读取aijson.json文件
file_path = r"C:/Users/EDY/Desktop/soulStation/crawler/aijson.json"
with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"共找到 {len(data)} 个主分类")

# 处理每个主分类
for main_item in data:
    # 创建主分类
    main_title = main_item["title"][:20]  # 截断到最大长度20
    main_content = main_item["content"][:500] if main_item["content"] else ""  # 截断到最大长度500
    
    # 保存主分类到数据库
    main_category = PsychologicalKnowledge(
        title=main_title,
        content=main_content,
        is_active=True
    )
    main_category.save()
    
    print(f"主分类 '{main_title}' 已保存到数据库，ID: {main_category.id}")
    
    # 处理子分类
    if "childrens" in main_item and main_item["childrens"]:
        for children_item in main_item["childrens"]:
            # 第一级子节点
            children_title = children_item["title"][:20]  # 截断到最大长度20
            children_content = children_item["content"][:500] if children_item["content"] else ""  # 截断到最大长度500
            
            # 第一级子节点的parent_title为主分类title
            children_detail = PsychologicalKnowledgeDetail(
                title=children_title,
                content=children_content,
                parent_id=str(main_category.id),  # 父id为主分类的id
                parent_title=main_title,  # 父节点title为主分类title
                is_active=True
            )
            children_detail.save()
            
            print(f"  第一级子分类 '{children_title}' 已保存到数据库")
            
            # 处理第二级及更深层次的子节点
            if "childrens" in children_item and children_item["childrens"]:
                for deeper_item in children_item["childrens"]:
                    # 第二级节点开始的父节点title为其父节点的title，父id还是为主分类的id
                    deeper_title = deeper_item["title"][:20]  # 截断到最大长度20
                    deeper_content = deeper_item["content"][:500] if deeper_item["content"] else ""  # 截断到最大长度500
                    
                    deeper_detail = PsychologicalKnowledgeDetail(
                        title=deeper_title,
                        content=deeper_content,
                        parent_id=str(main_category.id),  # 父id还是为主分类的id
                        parent_title=children_title,  # 父节点title为其父节点的title
                        is_active=True
                    )
                    deeper_detail.save()
                    
                    print(f"    第二级子分类 '{deeper_title}' 已保存到数据库")
                    
                    # 处理第三级及更深层次的子节点（如果有的话）
                    if "childrens" in deeper_item and deeper_item["childrens"]:
                        for deepest_item in deeper_item["childrens"]:
                            deepest_title = deepest_item["title"][:20]  # 截断到最大长度20
                            deepest_content = deepest_item["content"][:500] if deepest_item["content"] else ""  # 截断到最大长度500
                            
                            deepest_detail = PsychologicalKnowledgeDetail(
                                title=deepest_title,
                                content=deepest_content,
                                parent_id=str(main_category.id),  # 父id还是为主分类的id
                                parent_title=deeper_title,  # 父节点title为其父节点的title
                                is_active=True
                            )
                            deepest_detail.save()
                            
                            print(f"      第三级子分类 '{deepest_title}' 已保存到数据库")

print("\n所有数据已成功保存到数据库！")
