<template>
    <div class="container">
        <div class="row">
            <Video class="col-6" />
            <Choice class="col-6" />
        </div>
    </div>
</template>

<script>
import Video from '@/components/Video.vue'
import Choice from '@/components/Choice.vue'

export default {
    name: "Mode",
    components: { Video, Choice }
}
</script>
