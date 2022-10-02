<template>
    <div class="full-HD">
        <section class="left">
            <keep-alive>
                <component :is="leftComponent"></component>
            </keep-alive>
        </section>
        <section class="right">
            <component :is="rightComponent" @update-component="setRightComponent"></component>
        </section>
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import Menu from '@/components/shared/Menu.vue';
import SkinColor from '@/components/shared/SkinColor.vue';
import Event from '@/components/mode/Event.vue';
import Custom from '@/components/mode/Custom.vue';

export default {
    name: "Settings",
    data: function () {
        return {
            leftComponent: Video,
            rightComponent: Menu
        };
    },
    methods: {
        setRightComponent(component) {
            this.rightComponent=component
        }
    },
    components: { Video, Menu, SkinColor, Event, Custom }
}
</script>

<style scoped>
.full-HD {
    display: grid;
    grid-template-columns: 960px 960px;
    grid-template-rows: 1080px;
    grid-template-areas:
        "left right";
}

.left {
    grid-area: left;
}

.right {
    grid-area: right;
}
</style>
