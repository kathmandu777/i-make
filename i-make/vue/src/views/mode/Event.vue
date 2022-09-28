<template>
    <div class="container">
        <div :style="{ display: 'flex', 'justify-content': 'space-around' }">
            <Video :style="{ flex: 1 }"/>
            <EventImageChoices :style="{ flex: 1 }" />
        </div>
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
