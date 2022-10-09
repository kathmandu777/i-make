<template>
    <SingleEffect :modeIconPath="kwargs.modeIconPath">Event Mode</SingleEffect>
</template>

<script>
import SingleEffect from '@/components/templates/SingleEffect.vue'

export default {
    name: 'Event',
    props: ['kwargs'],
    components: { SingleEffect },
}
</script>
