<template>
    <div class="full-HD">
        <section class="left">
            <keep-alive>
                <Video />
            </keep-alive>
        </section>
        <section class="right">
            <component
                :is="rightComponent"
                @update-component="setRightComponent"
                :kwargs="kwargs"
            ></component>
        </section>
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import Menu from '@/components/shared/Menu.vue'
import SkinColor from '@/components/shared/SkinColor.vue'
import Event from '@/components/mode/Event.vue'
import Easy from '@/components/mode/Easy.vue'
import Custom from '@/components/mode/custom/Custom.vue'
import CustomChoices from '@/components/mode/custom/CustomChoices.vue'
import Practice from '@/components/mode/Practice.vue'
import Diagnosis from '@/components/mode/Diagnosis.vue'

export default {
    name: 'Settings',
    data: function () {
        return {
            rightComponent: Menu,
            kwargs: {},
        }
    },
    methods: {
        setRightComponent(component, kwargs) {
            this.rightComponent = component
            this.kwargs = kwargs
        },
    },
    components: {
        Video,
        Menu,
        SkinColor,
        Event,
        Custom,
        CustomChoices,
        Easy,
        Practice,
        Diagnosis,
    },
}
</script>

<style>
* {
    background-color: black;
    color: white;
}

body {
    padding: 0;
    margin: 0;
}
</style>

<style scoped>
.full-HD {
    display: grid;
    grid-template-columns: 960px 960px;
    grid-template-rows: 1080px;
    grid-template-areas: 'left right';
}

.left {
    grid-area: left;
}

.right {
    grid-area: right;
}
</style>
