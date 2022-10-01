<template>
    <div class="container">
        <Video class="video" />
        <SkinColor class="content" />
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import SkinColor from '@/components/shared/SkinColor.vue';

export default {
    name: "Settings",
    components: { Video, SkinColor }
}
</script>

<style scoped>
.container {
    display: grid;
    grid-template-columns: 960px 960px;
    grid-template-rows: 1080px;
    grid-template-areas:
        "video contentarea";
}

.video {
    grid-area: video;
}

.content {
    grid-area: contentarea;
}
</style>
