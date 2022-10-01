<template>
    <div class="container">
        <Video class="video" />
        <DiagnosisChoices class="content" />
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import DiagnosisChoices from '@/components/mode/diagnosis/DiagnosisChoices.vue'

export default {
    name: "Mode",
    components: { Video, DiagnosisChoices }
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
