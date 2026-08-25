"""
物品堆叠组件映射表
用于将旧的NBT标签转换为1.20.5+的新组件格式
"""

# 旧NBT标签到新组件的映射
NBT_TO_COMPONENT = {
    # 显示属性
    "display.Name": "minecraft:custom_name",
    "display.Lore": "minecraft:lore",
    "display.color": "minecraft:dyed_color",
    
    # 附魔
    "Enchantments": "minecraft:enchantments",
    
    # 属性修饰符
    "AttributeModifiers": "minecraft:attribute_modifiers",
    
    # 药水
    "CustomPotionEffects": "minecraft:potion_contents",
    "CustomPotionColor": "minecraft:potion_contents.custom_color",
    
    # 烟花
    "Fireworks": "minecraft:fireworks",
    
    # 其他属性
    "Unbreakable": "minecraft:unbreakable",
    "Damage": "minecraft:damage",
    "CustomModelData": "minecraft:custom_model_data",
    "HideFlags": "minecraft:hide_flags",
    
    # 特殊能力
    "CanDestroy": "minecraft:can_break",
    "CanPlaceOn": "minecraft:can_place_on",
}

# 组件格式化函数
def format_enchantments_component(enchantments):
    """
    将附魔列表转换为组件格式
    旧格式: [{"id": "minecraft:sharpness", "lvl": 5}]
    新格式: {"minecraft:sharpness": 5}
    """
    if not enchantments:
        return None
    
    result = {}
    for enchant in enchantments:
        enchant_id = enchant["id"]
        # 移除 minecraft: 前缀，使用纯附魔名称
        if enchant_id.startswith("minecraft:"):
            enchant_id = enchant_id[10:]
        level = enchant["lvl"]
        result[enchant_id] = level
    
    return result

def format_custom_name_component(name_json):
    """
    将自定义名称转换为组件格式
    旧格式: {"text": "名称", "color": "red", "bold": true}
    新格式: {type: "text", text: "名称", color: "red", bold: true}
    """
    if not name_json:
        return None
    
    # 确保有type字段
    if "type" not in name_json:
        name_json["type"] = "text"
    
    return name_json

def format_lore_component(lore_list):
    """
    将描述列表转换为组件格式
    旧格式: ["{\"text\": \"描述1\"}", "{\"text\": \"描述2\"}"]
    新格式: ["{\"text\": \"描述1\"}", "{\"text\": \"描述2\"}"]
    """
    if not lore_list:
        return None
    
    return lore_list

def format_attribute_modifiers_component(attributes):
    """
    将属性修饰符转换为组件格式
    旧格式: [{"AttributeName": "generic.attack_damage", "Name": "noName", "Amount": 5, "Operation": 0, "UUID": [...], "Slot": "mainhand"}]
    新格式: [{"key": "custom", "type": "minecraft:generic.attack_damage", "amount": 5, "operation": "add_value", "slot": "mainhand"}]
    """
    if not attributes:
        return None
    
    result = []
    operation_map = {
        0: "add_value",
        1: "add_multiplied_base",
        2: "add_multiplied_total"
    }
    
    for attr in attributes:
        # 移除 minecraft: 前缀和 generic. 前缀，使用纯属性名称
        attr_id = attr["AttributeName"].replace("minecraft:", "").replace("generic.", "")
        modifier = {
            "id": "custom",
            "type": attr_id,  # 使用不带前缀的纯属性名称
            "amount": attr["Amount"],
            "operation": operation_map.get(attr["Operation"], "add_value"),
            "slot": attr["Slot"]
        }
        result.append(modifier)
    
    return result

def format_potion_contents_component(effects, color):
    """
    将药水效果转换为组件格式
    旧格式: CustomPotionEffects: [...], CustomPotionColor: 123456
    新格式: {custom_effects: [...], custom_color: 123456}
    """
    # 只有在有效果时才生成药水内容组件
    if not effects:
        return None
    
    result = {}
    
    # 转换效果格式
    effect_map = {
        1: "minecraft:speed",
        2: "minecraft:slowness",
        3: "minecraft:haste",
        4: "minecraft:mining_fatigue",
        5: "minecraft:strength",
        6: "minecraft:instant_health",
        7: "minecraft:instant_damage",
        8: "minecraft:jump_boost",
        9: "minecraft:nausea",
        10: "minecraft:regeneration",
        11: "minecraft:resistance",
        12: "minecraft:fire_resistance",
        13: "minecraft:water_breathing",
        14: "minecraft:invisibility",
        15: "minecraft:blindness",
        16: "minecraft:night_vision",
        17: "minecraft:hunger",
        18: "minecraft:weakness",
        19: "minecraft:poison",
        20: "minecraft:wither",
        21: "minecraft:health_boost",
        22: "minecraft:absorption",
        23: "minecraft:saturation",
        24: "minecraft:luck",
        25: "minecraft:slow_falling",
        26: "minecraft:conduit_power",
        27: "minecraft:dolphins_grace",
        28: "minecraft:bad_omen",
        29: "minecraft:hero_of_the_village",
        30: "minecraft:darkness"
    }
    
    custom_effects = []
    for effect in effects:
        effect_id = effect["Id"]
        effect_name = effect_map.get(effect_id, f"minecraft:unknown_{effect_id}")
        effect_data = {
            "id": effect_name,
            "amplifier": effect["Amplifier"],
            "duration": effect["Duration"],
            "show_particles": effect["ShowParticles"],
            "ambient": effect["Ambient"]
        }
        custom_effects.append(effect_data)
    
    result["custom_effects"] = custom_effects
    
    if color:
        result["custom_color"] = color
    
    return result

def format_fireworks_component(fireworks_data):
    """
    将烟花数据转换为组件格式
    旧格式: {Flight: 1, Explosions: [...]}
    新格式: {flight_duration: 1, explosions: [...]}
    """
    if not fireworks_data:
        return None
    
    result = {}
    
    # 支持新旧两种键名
    flight_key = "flight_duration" if "flight_duration" in fireworks_data else "Flight"
    if flight_key in fireworks_data:
        result["flight_duration"] = fireworks_data[flight_key]
    
    explosions_key = "explosions" if "explosions" in fireworks_data else "Explosions"
    if explosions_key in fireworks_data:
        result["explosions"] = fireworks_data[explosions_key]
    
    return result

def format_other_components(unbreakable, damage, model_data, hide_flags):
    """
    将其他属性转换为组件格式
    """
    components = {}
    
    if unbreakable:
        components["minecraft:unbreakable"] = {}
    
    if damage:
        try:
            components["minecraft:damage"] = int(damage)
        except ValueError:
            pass
    
    if model_data:
        try:
            components["minecraft:custom_model_data"] = int(model_data)
        except ValueError:
            pass
    
    if hide_flags:
        try:
            components["minecraft:hide_flags"] = int(hide_flags)
        except ValueError:
            pass
    
    return components if components else None

def format_food_component(food_data):
    """
    将食物数据转换为组件格式
    格式: {nutrition: 整数, saturation: 浮点数, can_always_eat: 布尔值}
    """
    if not food_data:
        return None
    
    result = {
        "nutrition": food_data.get("nutrition", 0),
        "saturation": food_data.get("saturation", 0.0),
        "can_always_eat": food_data.get("can_always_eat", False)
    }
    
    return result

def format_consumable_component(consumable_data):
    """
    将消耗品数据转换为组件格式
    格式: {consume_seconds: 浮点数, animation: 字符串, sound: 字符串, has_consume_particles: 布尔值, on_consume_effects: [...]}
    """
    if not consumable_data:
        return None
    
    result = {
        "consume_seconds": consumable_data.get("consume_seconds", 1.6),
        "animation": consumable_data.get("animation", "eat"),
        "sound": consumable_data.get("sound", "entity.generic.eat")
    }
    
    # 只有当has_consume_particles为false时才添加
    has_consume_particles = consumable_data.get("has_consume_particles", True)
    if not has_consume_particles:
        result["has_consume_particles"] = has_consume_particles
    
    # 只有当on_consume_effects不为空时才添加
    on_consume_effects = consumable_data.get("on_consume_effects", [])
    if on_consume_effects:
        result["on_consume_effects"] = on_consume_effects
    
    return result

def format_banner_component(banner_data):
    """
    将旗帜数据转换为组件格式
    组件名称: minecraft:banner_patterns
    格式: [{pattern: "base", color: "white"}]
    直接返回图案列表，不包含patterns键
    """
    if not banner_data:
        return None
    
    # 直接返回图案列表，不包含patterns键
    patterns = banner_data.get("patterns", [])
    if patterns:
        return patterns
    
    return None

def format_tool_component(tool_data):
    """
    将工具数据转换为组件格式
    组件名称: tool
    格式: {default_mining_speed: 1.0, damage_per_block: 1, rules: [...]}
    确保即使没有规则也包含空的rules列表
    """
    if not tool_data:
        return None
    
    result = {}
    
    # 默认挖掘速度
    default_mining_speed = tool_data.get("default_mining_speed")
    if default_mining_speed is not None:
        result["default_mining_speed"] = default_mining_speed
    
    # 每方块消耗耐久度
    damage_per_block = tool_data.get("damage_per_block")
    if damage_per_block is not None:
        result["damage_per_block"] = damage_per_block
    
    # 挖掘规则 - 确保始终包含rules键，即使为空
    rules = tool_data.get("rules", [])
    result["rules"] = rules
    
    return result

def format_written_book_component(book_data):
    """
    将成书数据转换为组件格式
    组件名称: written_book_content
    格式: {pages: [...], title: "书名", author: "作者", generation: 0}
    """
    if not book_data:
        return None
    
    result = {}
    
    # 页面内容
    pages = book_data.get("pages")
    if pages:
        result["pages"] = pages
    
    # 书名
    title = book_data.get("title")
    if title:
        result["title"] = title
    
    # 作者
    author = book_data.get("author")
    if author:
        result["author"] = author
    
    # 生成类型 (0: 原创, 1: 副本, 2: 副本的副本, 3: 破损)
    generation = book_data.get("generation", 0)
    result["generation"] = generation
    
    return result

def format_equippable_component(equippable_data):
    """
    将装备数据转换为组件格式
    组件名称: equippable
    格式: {slot: "chest", equip_sound: "id", model: "id", camera_overlay: "id", allowed_entities: [...], dispensable: 1b, swappable: 1b, damage_on_hurt: 0b, glider: 1b, death_protection: 1b}
    
    参数说明：
    - slot: 装备槽位 (head/chest/legs/feet/body/mainhand/offhand)
    - equip_sound: 装备声音事件ID（可选），未指定时使用默认装备声音事件
    - model: 装备模型ID（可选）
    - camera_overlay: 相机遮罩纹理ID（可选），当物品被玩家穿戴时，玩家第一人称视角将渲染指定的纹理遮罩
    - allowed_entities: 允许装备的实体列表（可选），限制哪些实体可以装备此物品
    - dispensable: 可被发射器装备 (1b/0b)
    - swappable: 可交换 (1b/0b)
    - damage_on_hurt: 受伤时受损 (1b/0b)
    - glider: 滑翔功能，允许物品像鞘翅一样滑翔 (1b/0b)
    - death_protection: 死亡保护，死亡时消耗此物品并保留物品栏 (1b/0b)
    """
    if not equippable_data:
        return None
    
    result = {}
    
    # 装备槽位
    slot = equippable_data.get("slot")
    if slot:
        result["slot"] = slot
    
    # 装备声音
    equip_sound = equippable_data.get("equip_sound")
    if equip_sound:
        result["equip_sound"] = equip_sound
    
    # 装备模型
    model = equippable_data.get("model")
    if model:
        result["model"] = model
    
    # 相机遮罩
    camera_overlay = equippable_data.get("camera_overlay")
    if camera_overlay:
        result["camera_overlay"] = camera_overlay
    
    # 允许的实体
    allowed_entities = equippable_data.get("allowed_entities")
    if allowed_entities:
        result["allowed_entities"] = allowed_entities
    
    # 可被发射器装备
    dispensable = equippable_data.get("dispensable")
    if dispensable is not None:
        result["dispensable"] = 1 if dispensable else 0
    
    # 可交换
    swappable = equippable_data.get("swappable")
    if swappable is not None:
        result["swappable"] = 1 if swappable else 0
    
    # 受伤时受损
    damage_on_hurt = equippable_data.get("damage_on_hurt")
    if damage_on_hurt is not None:
        result["damage_on_hurt"] = 1 if damage_on_hurt else 0
    
    # 滑翔功能
    glider = equippable_data.get("glider")
    if glider:
        result["glider"] = 1
    
    # 死亡保护
    death_protection = equippable_data.get("death_protection")
    if death_protection:
        result["death_protection"] = 1
    
    return result
