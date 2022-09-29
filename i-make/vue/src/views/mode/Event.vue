<template>
    <div class="container">
        <Video class="video" />
        <EventImageChoices class="content" />
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import EventImageChoices from '@/components/mode/event/EventImageChoices.vue'

export default {
    name: "Mode",
    components: { Video, EventImageChoices }
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
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 1080px;
    margin: 0;
}
</style>