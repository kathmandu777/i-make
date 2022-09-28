<template>
    <div>
        <div :style="{ display: 'flex', 'justify-content': 'space-around' }">
            <Video :style="{ flex: 1 }"/>
            <Choice :style="{ flex: 1 }" />
        </div>
    </div>
</template>

<script>
import Video from '@/components/shared/Video.vue'
import Choice from '@/components/Choice.vue'

export default {
    name: "Mode",
    components: { Video, Choice }
}
</script>
