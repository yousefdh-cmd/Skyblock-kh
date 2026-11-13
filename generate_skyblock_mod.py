#!/usr/bin/env python3
"""
مولّد مشروع NeoForge 1.21.1 - SkyBlock Core v7.0 (الجزء 1 من 4)
نظام مستويات عشوائية (1-2000) مع ندرة متزايدة للمستويات العالية.
"""

from pathlib import Path

ROOT = Path("skyblockcore").resolve()

FILES = {

"settings.gradle": """\
pluginManagement {
    repositories {
        maven { url = 'https://maven.neoforged.net/releases' }
        gradlePluginPortal()
    }
}
""",

"gradle.properties": """\
org.gradle.jvmargs=-Xmx2G
org.gradle.parallel=true
org.gradle.caching=true
""",

"build.gradle": """\
plugins {
    id 'java'
    id 'net.neoforged.moddev' version '2.0.78'
}

version = '7.0.0'
group = 'com.example.skyblockcore'

java.toolchain.languageVersion = JavaLanguageVersion.of(21)

neoForge {
    version = '21.1.172'
    parchment {
        minecraftVersion = '1.21.1'
        mappingsVersion = '2024.11.17'
    }
    runs {
        client { client() }
    }
    mods {
        skyblockcore { sourceSet sourceSets.main }
    }
}
""",

".gitignore": """\
.gradle/
build/
run/
*.iml
.idea/
""",

"src/main/resources/META-INF/neoforge.mods.toml": """\
modLoader="javafml"
loaderVersion="[4,)"
license="MIT"

[[mods]]
modId="skyblockcore"
version="7.0.0"
displayName="SkyBlock Core"
description="نظام مستويات عشوائية 1-2000 مع ندرة متزايدة."

[[dependencies.skyblockcore]]
    modId="neoforge"
    type="required"
    versionRange="[21.1.0,)"
    ordering="NONE"
    side="BOTH"

[[dependencies.skyblockcore]]
    modId="minecraft"
    type="required"
    versionRange="[1.21.1]"
    ordering="NONE"
    side="BOTH"
""",

"src/main/java/com/example/skyblockcore/SkyBlockCore.java": """\
package com.example.skyblockcore;

import com.mojang.logging.LogUtils;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.common.NeoForge;
import org.slf4j.Logger;

@Mod(SkyBlockCore.MODID)
public class SkyBlockCore {
    public static final String MODID = "skyblockcore";
    public static final Logger LOGGER = LogUtils.getLogger();

    public SkyBlockCore(IEventBus modBus) {
        SkyBlockRegistries.register(modBus);
        NeoForge.EVENT_BUS.register(SkyBlockEvents.class);
        LOGGER.info("SkyBlock Core v7.0 initialized (Random Levels 1-2000)!");
    }
}
""",

"src/main/java/com/example/skyblockcore/SkyBlockRegistries.java": """\
package com.example.skyblockcore;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.ai.attributes.Attribute;
import net.minecraft.world.entity.ai.attributes.RangedAttribute;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class SkyBlockRegistries {

    public static final DeferredRegister<Attribute> ATTRIBUTES =
            DeferredRegister.create(Registries.ATTRIBUTE, SkyBlockCore.MODID);

    public static final DeferredHolder<Attribute, Attribute> HEALTH =
            ATTRIBUTES.register("health", () ->
                    new RangedAttribute("attribute.skyblockcore.health", 100.0, 0.0, 100000.0).setSyncable(true));

    public static final DeferredHolder<Attribute, Attribute> DEFENSE =
            ATTRIBUTES.register("defense", () ->
                    new RangedAttribute("attribute.skyblockcore.defense", 0.0, 0.0, 100000.0).setSyncable(true));

    public static final DeferredHolder<Attribute, Attribute> STRENGTH =
            ATTRIBUTES.register("strength", () ->
                    new RangedAttribute("attribute.skyblockcore.strength", 0.0, 0.0, 100000.0).setSyncable(true));

    public static final DeferredHolder<Attribute, Attribute> CRIT_CHANCE =
            ATTRIBUTES.register("crit_chance", () ->
                    new RangedAttribute("attribute.skyblockcore.crit_chance", 30.0, 0.0, 100.0).setSyncable(true));

    public static final DeferredHolder<Attribute, Attribute> CRIT_DAMAGE =
            ATTRIBUTES.register("crit_damage", () ->
                    new RangedAttribute("attribute.skyblockcore.crit_damage", 50.0, 0.0, 100000.0).setSyncable(true));

    public static final DeferredHolder<Attribute, Attribute> FEROCITY =
            ATTRIBUTES.register("ferocity", () ->
                    new RangedAttribute("attribute.skyblockcore.ferocity", 0.0, 0.0, 500.0).setSyncable(true));

    public static void register(IEventBus modBus) {
        ATTRIBUTES.register(modBus);
    }
}
""",

"src/main/java/com/example/skyblockcore/SkyBlockMechanics.java": """\
package com.example.skyblockcore;

public final class SkyBlockMechanics {

    /**
     * توليد مستوى عشوائي بين 1 و 2000.
     * التوزيع: Math.pow(random, 5) يجعل المستويات العالية نادرة جداً.
     * مثال: المستوى 1000 أو أعلى يظهر بنسبة ~13% فقط.
     */
    public static int getRandomLevel() {
        double random = Math.random();
        // pow(random, 5) يضمن أن معظم القيم قريبة من 0 (مستويات منخفضة)
        int level = (int) Math.floor(Math.pow(random, 5) * 2000) + 1;
        return Math.min(2000, Math.max(1, level));
    }

    /**
     * مضاعف الصحة بناءً على المستوى.
     * المستوى 1: ~1.0x | المستوى 1000: ~201x | المستوى 2000: ~401x
     */
    public static double getHealthMultiplier(int level) {
        return 1.0 + (level * 0.2);
    }

    /**
     * مضاعف الضرر بناءً على المستوى.
     * المستوى 1: ~1.0x | المستوى 1000: ~101x | المستوى 2000: ~201x
     */
    public static double getDamageMultiplier(int level) {
        return 1.0 + (level * 0.1);
    }

    /**
     * صيغة الضرر الأساسية من SkyBlock (بدون تعديل).
     */
    public static double calculatePlayerDamage(double weaponDamage, double strength,
                                                double critDamage, boolean isCritical) {
        double base = (5.0 + weaponDamage) * (1.0 + (strength / 100.0));
        if (isCritical) base *= (1.0 + (critDamage / 100.0));
        return Math.floor(base);
    }

    /**
     * تقليل الضرر بناءً على Defense.
     */
    public static double applyDefenseReduction(double incomingDamage, double defense) {
        if (defense <= 0) return incomingDamage;
        return incomingDamage * (1.0 - (defense / (defense + 100.0)));
    }
}
""",
}

FILES.update({

"src/main/java/com/example/skyblockcore/SkyBlockEvents.java": """\
package com.example.skyblockcore;

import net.minecraft.network.chat.Component;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.EquipmentSlotGroup;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.AxeItem;
import net.minecraft.world.item.ArmorItem;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.item.SwordItem;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.ItemAttributeModifierEvent;
import net.neoforged.neoforge.event.entity.EntityJoinLevelEvent;
import net.neoforged.neoforge.event.entity.living.LivingIncomingDamageEvent;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;

public final class SkyBlockEvents {

    @SubscribeEvent
    public static void onPlayerLogin(PlayerEvent.PlayerLoggedInEvent event) {
        Player player = event.getEntity();
        var hp = player.getAttribute(Attributes.MAX_HEALTH);
        if (hp != null) { hp.setBaseValue(100.0); player.setHealth(100.0f); }
    }

    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().getEntity() instanceof Player player) {
            double weaponDamage = 3.0;
            ItemStack weapon = player.getMainHandItem();
            if (weapon.getItem() instanceof SwordItem sword) weaponDamage = sword.getDamage();
            else if (weapon.getItem() instanceof AxeItem axe) weaponDamage = axe.getDamage();

            var strInst = player.getAttribute(SkyBlockRegistries.STRENGTH);
            var ccInst = player.getAttribute(SkyBlockRegistries.CRIT_CHANCE);
            var cdInst = player.getAttribute(SkyBlockRegistries.CRIT_DAMAGE);
            var ferInst = player.getAttribute(SkyBlockRegistries.FEROCITY);

            double strength = strInst != null ? strInst.getValue() : 0.0;
            double critChance = ccInst != null ? ccInst.getValue() : 30.0;
            double critDamage = cdInst != null ? cdInst.getValue() : 50.0;
            double ferocity = ferInst != null ? ferInst.getValue() : 0.0;

            boolean isCrit = player.getRandom().nextFloat() * 100.0f < critChance;
            double finalDmg = SkyBlockMechanics.calculatePlayerDamage(weaponDamage, strength, critDamage, isCrit);
            if (ferocity > 0) {
                int extraHits = (int) (ferocity / 100.0);
                if (player.getRandom().nextFloat() * 100.0f < (ferocity % 100.0)) extraHits++;
                finalDmg *= (1 + extraHits);
            }
            event.setAmount((float) finalDmg);
            return;
        }

        if (event.getEntity() instanceof Player player) {
            var defInst = player.getAttribute(SkyBlockRegistries.DEFENSE);
            double defense = defInst != null ? defInst.getValue() : 0.0;
            if (defense > 0) {
                event.setAmount((float) SkyBlockMechanics.applyDefenseReduction(event.getAmount(), defense));
            }
        }
    }

    @SubscribeEvent
    public static void onEntityJoin(EntityJoinLevelEvent event) {
        if (event.getLevel().isClientSide()) return;
        if (!(event.getEntity() instanceof LivingEntity mob)) return;
        if (mob instanceof Player) return;

        var hpAttr = mob.getAttribute(Attributes.MAX_HEALTH);
        if (hpAttr == null) return;

        // مستوى عشوائي (1-2000) - كلما زاد، زادت ندرته
        int level = SkyBlockMechanics.getRandomLevel();

        // مضاعفة الصحة بناءً على المستوى
        double baseHp = hpAttr.getBaseValue();
        double newHp = baseHp * SkyBlockMechanics.getHealthMultiplier(level);
        hpAttr.setBaseValue(newHp);
        mob.setHealth((float) newHp);

        // مضاعفة الضرر (إن كان للوحش ضرر)
        var dmgAttr = mob.getAttribute(Attributes.ATTACK_DAMAGE);
        if (dmgAttr != null) {
            double baseDmg = dmgAttr.getBaseValue();
            dmgAttr.setBaseValue(baseDmg * SkyBlockMechanics.getDamageMultiplier(level));
        }

        // عرض المستوى فوق رأس الوحش
        String name = mob.getName().getString();
        mob.setCustomName(Component.literal("§8[§7Lv" + level + "§8] §f" + name));
        mob.setCustomNameVisible(true);
    }

    @SubscribeEvent
    public static void onItemAttributes(ItemAttributeModifierEvent event) {
        ItemStack stack = event.getItemStack();
        Item item = stack.getItem();

        // ===== السيوف =====
        if (item instanceof SwordItem) {
            double damage = 0;
            if (item == Items.WOODEN_SWORD) damage = 20;
            else if (item == Items.STONE_SWORD) damage = 25;
            else if (item == Items.GOLDEN_SWORD) damage = 20;
            else if (item == Items.IRON_SWORD) damage = 30;
            else if (item == Items.DIAMOND_SWORD) damage = 35;
            else if (item == Items.NETHERITE_SWORD) damage = 40;
            if (damage > 0) {
                event.addModifier(Attributes.ATTACK_DAMAGE,
                    new AttributeModifier(ResourceLocation.fromNamespaceAndPath(SkyBlockCore.MODID, "sb_sword_dmg"),
                        damage, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND);
            }
        }

        // ===== الفؤوس =====
        if (item instanceof AxeItem) {
            double damage = 0;
            if (item == Items.WOODEN_AXE) damage = 10;
            else if (item == Items.STONE_AXE) damage = 15;
            else if (item == Items.GOLDEN_AXE) damage = 20;
            else if (item == Items.IRON_AXE) damage = 25;
            else if (item == Items.DIAMOND_AXE) damage = 30;
            else if (item == Items.NETHERITE_AXE) damage = 35;
            if (damage > 0) {
                event.addModifier(Attributes.ATTACK_DAMAGE,
                    new AttributeModifier(ResourceLocation.fromNamespaceAndPath(SkyBlockCore.MODID, "sb_axe_dmg"),
                        damage, AttributeModifier.Operation.ADD_VALUE), EquipmentSlotGroup.MAINHAND);
            }
        }

        // ===== الدروع =====
        if (item instanceof ArmorItem armor) {
            EquipmentSlotGroup group = EquipmentSlotGroup.bySlot(armor.getEquipmentSlot());
            double defense = 0;

            if (item == Items.LEATHER_HELMET) defense = 6;
            else if (item == Items.LEATHER_CHESTPLATE) defense = 15;
            else if (item == Items.LEATHER_LEGGINGS) defense = 10;
            else if (item == Items.LEATHER_BOOTS) defense = 5;
            else if (item == Items.GOLDEN_HELMET) defense = 10;
            else if (item == Items.GOLDEN_CHESTPLATE) defense = 25;
            else if (item == Items.GOLDEN_LEGGINGS) defense = 15;
            else if (item == Items.GOLDEN_BOOTS) defense = 5;
            else if (item == Items.CHAINMAIL_HELMET) defense = 12;
            else if (item == Items.CHAINMAIL_CHESTPLATE) defense = 30;
            else if (item == Items.CHAINMAIL_LEGGINGS) defense = 20;
            else if (item == Items.CHAINMAIL_BOOTS) defense = 7;
            else if (item == Items.IRON_HELMET) defense = 12;
            else if (item == Items.IRON_CHESTPLATE) defense = 30;
            else if (item == Items.IRON_LEGGINGS) defense = 25;
            else if (item == Items.IRON_BOOTS) defense = 10;
            else if (item == Items.DIAMOND_HELMET) defense = 15;
            else if (item == Items.DIAMOND_CHESTPLATE) defense = 40;
            else if (item == Items.DIAMOND_LEGGINGS) defense = 30;
            else if (item == Items.DIAMOND_BOOTS) defense = 15;
            else if (item == Items.NETHERITE_HELMET) defense = 20;
            else if (item == Items.NETHERITE_CHESTPLATE) defense = 45;
            else if (item == Items.NETHERITE_LEGGINGS) defense = 35;
            else if (item == Items.NETHERITE_BOOTS) defense = 20;
            else if (item == Items.TURTLE_HELMET) defense = 10;

            if (defense > 0) {
                event.addModifier(Attributes.ARMOR,
                    new AttributeModifier(ResourceLocation.fromNamespaceAndPath(SkyBlockCore.MODID, "sb_armor_def"),
                        defense, AttributeModifier.Operation.ADD_VALUE), group);
            }
        }
    }
}
""",
})

def main():
    if ROOT.exists() and any(ROOT.iterdir()):
        print(f"WARNING: {ROOT} exists. Delete it first.")
        return
    for rel_path, content in FILES.items():
        target = ROOT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"OK {rel_path}")
    print(f"\\nDone. Project at: {ROOT}")

if __name__ == "__main__":
    main()
