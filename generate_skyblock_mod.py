#!/usr/bin/env python3
"""
مولّد مشروع NeoForge 1.21.1 - SkyBlock Core v3.0
يُنشئ مشروعاً كاملاً يطبق خصائص Combat Stats، صيغ الضرر،
مستوى الوحوش، وتعديل عناصر الفانيلا (سيف الماس، درع الماس).
يشغّل: python generate_skyblock_mod.py
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

version = '3.0.0'
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
        server { server() }
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
version="3.0.0"
displayName="SkyBlock Core"
description="Combat Stats كاملة + صيغ الضرر ومستوى الوحوش + تعديل عناصر الفانيلا."

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

# ============================================================
# Java
# ============================================================

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
        NeoForge.EVENT_BUS.register(SkyBlockCommands.class);
        LOGGER.info("SkyBlock Core v3.0 initialized!");
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

    // Health: 100 (SkyBlock base)
    public static final DeferredHolder<Attribute, Attribute> HEALTH =
            ATTRIBUTES.register("health", () ->
                    new RangedAttribute("attribute.skyblockcore.health", 100.0, 0.0, 100000.0)
                            .setSyncable(true));

    // Defense: 0
    public static final DeferredHolder<Attribute, Attribute> DEFENSE =
            ATTRIBUTES.register("defense", () ->
                    new RangedAttribute("attribute.skyblockcore.defense", 0.0, 0.0, 100000.0)
                            .setSyncable(true));

    // True Defense: 0
    public static final DeferredHolder<Attribute, Attribute> TRUE_DEFENSE =
            ATTRIBUTES.register("true_defense", () ->
                    new RangedAttribute("attribute.skyblockcore.true_defense", 0.0, 0.0, 100000.0)
                            .setSyncable(true));

    // Strength: 0
    public static final DeferredHolder<Attribute, Attribute> STRENGTH =
            ATTRIBUTES.register("strength", () ->
                    new RangedAttribute("attribute.skyblockcore.strength", 0.0, 0.0, 100000.0)
                            .setSyncable(true));

    // Crit Chance: 30%
    public static final DeferredHolder<Attribute, Attribute> CRIT_CHANCE =
            ATTRIBUTES.register("crit_chance", () ->
                    new RangedAttribute("attribute.skyblockcore.crit_chance", 30.0, 0.0, 100.0)
                            .setSyncable(true));

    // Crit Damage: 50%
    public static final DeferredHolder<Attribute, Attribute> CRIT_DAMAGE =
            ATTRIBUTES.register("crit_damage", () ->
                    new RangedAttribute("attribute.skyblockcore.crit_damage", 50.0, 0.0, 100000.0)
                            .setSyncable(true));

    // Ferocity: 0
    public static final DeferredHolder<Attribute, Attribute> FEROCITY =
            ATTRIBUTES.register("ferocity", () ->
                    new RangedAttribute("attribute.skyblockcore.ferocity", 0.0, 0.0, 500.0)
                            .setSyncable(true));

    // Attack Speed: 0
    public static final DeferredHolder<Attribute, Attribute> ATTACK_SPEED =
            ATTRIBUTES.register("attack_speed", () ->
                    new RangedAttribute("attribute.skyblockcore.attack_speed", 0.0, 0.0, 100.0)
                            .setSyncable(true));

    // Intelligence: 0
    public static final DeferredHolder<Attribute, Attribute> INTELLIGENCE =
            ATTRIBUTES.register("intelligence", () ->
                    new RangedAttribute("attribute.skyblockcore.intelligence", 0.0, 0.0, 100000.0)
                            .setSyncable(true));

    // Health Regen: 100
    public static final DeferredHolder<Attribute, Attribute> HEALTH_REGEN =
            ATTRIBUTES.register("health_regen", () ->
                    new RangedAttribute("attribute.skyblockcore.health_regen", 100.0, 0.0, 100000.0)
                            .setSyncable(true));

    public static void register(IEventBus modBus) {
        ATTRIBUTES.register(modBus);
    }
}
""",

"src/main/java/com/example/skyblockcore/SkyBlockMechanics.java": """\
package com.example.skyblockcore;

/**
 * صيغ Hypixel SkyBlock الرسمية.
 * - Damage = floor( (5 + WeaponDMG) * (1 + Strength/100) * (1 + CritDamage/100) )
 * - Defense Reduction = Defense / (Defense + 100)
 * - Effective Health = Health * (1 + Defense/100)
 * - Mob Level = floor( (log10(HP * DMG) - 2) ^ 2.6 )
 */
public final class SkyBlockMechanics {

    public static int calculateMobLevel(double health, double damage) {
        if (health <= 0 || damage <= 0) return 1;
        double log10 = Math.log10(health * damage);
        if (log10 < 2.0) return 1;
        double level = Math.pow(log10 - 2.0, 2.6);
        return Math.max(1, (int) Math.floor(level));
    }

    public static double calculatePlayerDamage(double weaponDamage, double strength,
                                                double critDamage, boolean isCritical) {
        double base = (5.0 + weaponDamage) * (1.0 + (strength / 100.0));
        if (isCritical) {
            base *= (1.0 + (critDamage / 100.0));
        }
        return Math.floor(base);
    }

    public static double applyDefenseReduction(double incomingDamage, double defense) {
        if (defense <= 0) return incomingDamage;
        double reduction = defense / (defense + 100.0);
        return incomingDamage * (1.0 - reduction);
    }

    public static double effectiveHealth(double health, double defense) {
        return health * (1.0 + (defense / 100.0));
    }
}
""",

"src/main/java/com/example/skyblockcore/SkyBlockEvents.java": """\
package com.example.skyblockcore;

import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.monster.Skeleton;
import net.minecraft.world.entity.monster.ZombieVillager;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
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
        if (hp != null) {
            hp.setBaseValue(100.0);
            player.setHealth(100.0f);
        }
    }

    @SubscribeEvent
    public static void onIncomingDamage(LivingIncomingDamageEvent event) {
        if (event.getSource().getEntity() instanceof Player player) {
            double weaponDamage = 3.0;
            if (player.getMainHandItem().is(Items.DIAMOND_SWORD)) {
                weaponDamage = 35.0;
            }

            double strength = getAttr(player, SkyBlockRegistries.STRENGTH);
            double critChance = getAttr(player, SkyBlockRegistries.CRIT_CHANCE);
            double critDamage = getAttr(player, SkyBlockRegistries.CRIT_DAMAGE);
            double ferocity = getAttr(player, SkyBlockRegistries.FEROCITY);

            boolean isCrit = player.getRandom().nextFloat() * 100.0f < critChance;
            double finalDmg = SkyBlockMechanics.calculatePlayerDamage(
                    weaponDamage, strength, critDamage, isCrit);

            if (ferocity > 0) {
                int extraHits = (int) (ferocity / 100.0);
                double extraChance = ferocity % 100.0;
                if (player.getRandom().nextFloat() * 100.0f < extraChance) {
                    extraHits += 1;
                }
                finalDmg *= (1 + extraHits);
            }

            event.setAmount((float) finalDmg);

            if (isCrit) {
                player.sendSystemMessage(Component.literal(
                        "§6✧ Critical! §c" + (int) finalDmg + " §7damage"));
            }
            return;
        }

        if (event.getEntity() instanceof Player player) {
            double defense = getAttr(player, SkyBlockRegistries.DEFENSE);
            double trueDefense = getAttr(player, SkyBlockRegistries.TRUE_DEFENSE);
            if (event.getSource().is(net.minecraft.world.damagesource.DamageTypes.GENERIC_KILL)) {
                return;
            }
            if (defense > 0) {
                float reduced = (float) SkyBlockMechanics.applyDefenseReduction(
                        event.getAmount(), defense);
                event.setAmount(reduced);
            }
        }
    }

    @SubscribeEvent
    public static void onEntityJoin(EntityJoinLevelEvent event) {
        if (event.getLevel().isClientSide()) return;
        if (!(event.getEntity() instanceof LivingEntity mob)) return;
        if (mob instanceof Player) return;

        double hp, dmg;
        if (mob instanceof Zombie) {
            hp = 100; dmg = 20;
        } else if (mob instanceof ZombieVillager) {
            hp = 120; dmg = 24;
        } else if (mob instanceof Skeleton) {
            hp = 100; dmg = 15;
        } else {
            return;
        }

        var hpAttr = mob.getAttribute(Attributes.MAX_HEALTH);
        var dmgAttr = mob.getAttribute(Attributes.ATTACK_DAMAGE);
        if (hpAttr == null || dmgAttr == null) return;

        hpAttr.setBaseValue(hp);
        dmgAttr.setBaseValue(dmg);
        mob.setHealth((float) hp);

        int level = SkyBlockMechanics.calculateMobLevel(hp, dmg);
        mob.setCustomName(Component.literal(
                "§8[§7Lv" + level + "§8] §f" + mob.getName().getString()));
        mob.setCustomNameVisible(true);
    }

    @SubscribeEvent
    public static void onItemAttributes(ItemAttributeModifierEvent event) {
        ItemStack stack = event.getItemStack();
        if (stack.is(Items.DIAMOND_SWORD)) {
            event.addModifier(Attributes.ATTACK_DAMAGE,
                    new net.minecraft.world.entity.ai.attributes.AttributeModifier(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                                    SkyBlockCore.MODID, "diamond_sword_damage"),
                            35.0,
                            net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE),
                    net.minecraft.world.entity.EquipmentSlotGroup.MAINHAND);
        }
        if (stack.is(Items.DIAMOND_HELMET)) {
            event.addModifier(Attributes.ARMOR,
                    new net.minecraft.world.entity.ai.attributes.AttributeModifier(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                                    SkyBlockCore.MODID, "diamond_helmet_def"),
                            15.0,
                            net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE),
                    net.minecraft.world.entity.EquipmentSlotGroup.HEAD);
        }
        if (stack.is(Items.DIAMOND_CHESTPLATE)) {
            event.addModifier(Attributes.ARMOR,
                    new net.minecraft.world.entity.ai.attributes.AttributeModifier(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                                    SkyBlockCore.MODID, "diamond_chest_def"),
                            40.0,
                            net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE),
                    net.minecraft.world.entity.EquipmentSlotGroup.CHEST);
        }
        if (stack.is(Items.DIAMOND_LEGGINGS)) {
            event.addModifier(Attributes.ARMOR,
                    new net.minecraft.world.entity.ai.attributes.AttributeModifier(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                                    SkyBlockCore.MODID, "diamond_legs_def"),
                            30.0,
                            net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE),
                    net.minecraft.world.entity.EquipmentSlotGroup.LEGS);
        }
        if (stack.is(Items.DIAMOND_BOOTS)) {
            event.addModifier(Attributes.ARMOR,
                    new net.minecraft.world.entity.ai.attributes.AttributeModifier(
                            net.minecraft.resources.ResourceLocation.fromNamespaceAndPath(
                                    SkyBlockCore.MODID, "diamond_boots_def"),
                            15.0,
                            net.minecraft.world.entity.ai.attributes.AttributeModifier.Operation.ADD_VALUE),
                    net.minecraft.world.entity.EquipmentSlotGroup.FEET);
        }
    }

    private static double getAttr(Player player,
                                  net.neoforged.neoforge.registries.DeferredHolder<Attribute, Attribute> holder) {
        var instance = player.getAttribute(holder);
        return instance != null ? instance.getValue() : 0.0;
    }
}
""",

"src/main/java/com/example/skyblockcore/SkyBlockCommands.java": """\
package com.example.skyblockcore;

import net.minecraft.client.Minecraft;
import net.minecraft.commands.Commands;
import net.minecraft.network.chat.Component;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.client.event.RegisterClientCommandsEvent;

public final class SkyBlockCommands {

    @SubscribeEvent
    public static void register(RegisterClientCommandsEvent event) {
        event.getDispatcher().register(
            Commands.literal("sbstats").executes(ctx -> {
                var player = Minecraft.getInstance().player;
                if (player == null) return 0;

                double hp = get(player, SkyBlockRegistries.HEALTH);
                double def = get(player, SkyBlockRegistries.DEFENSE);
                double str = get(player, SkyBlockRegistries.STRENGTH);
                double cc = get(player, SkyBlockRegistries.CRIT_CHANCE);
                double cd = get(player, SkyBlockRegistries.CRIT_DAMAGE);
                double fer = get(player, SkyBlockRegistries.FEROCITY);
                double ehp = SkyBlockMechanics.effectiveHealth(hp, def);

                player.sendSystemMessage(Component.literal(
                    "§a=== SkyBlock Stats ==="));
                player.sendSystemMessage(Component.literal(
                    "§c❤ Health: " + hp + " §7| §a🛡 Defense: " + def +
                    " §7| §2Effective HP: " + (int) ehp));
                player.sendSystemMessage(Component.literal(
                    "§c❁ Strength: " + str + " §7| §6☠ Crit Chance: " + cc +
                    "% §7| §6Crit Damage: " + cd + "%"));
                player.sendSystemMessage(Component.literal(
                    "§e⚡ Ferocity: " + fer + "%"));
                return 1;
            })
        );
    }

    private static double get(net.minecraft.world.entity.player.Player player,
                              net.neoforged.neoforge.registries.DeferredHolder<
                                      net.minecraft.world.entity.ai.attributes.Attribute,
                                      net.minecraft.world.entity.ai.attributes.Attribute> holder) {
        var inst = player.getAttribute(holder);
        return inst != null ? inst.getValue() : 0.0;
    }
}
""",
}

def main():
    if ROOT.exists() and any(ROOT.iterdir()):
        print(f"WARNING: {ROOT} exists and is not empty. Delete or rename it first.")
        return
    for rel_path, content in FILES.items():
        target = ROOT / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        print(f"OK {rel_path}")
    print(f"\\nDone. Project at: {ROOT}")
    print("Next steps:")
    print(f"  cd {ROOT.name}")
    print("  gradle wrapper --gradle-version 8.9")
    print("  ./gradlew runClient")

if __name__ == "__main__":
    main()
