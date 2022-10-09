<template>
    <SingleEffect :modeIconPath="kwargs.modeIconPath"
        >Practice Mode</SingleEffect
    >
</template>

<script>
import SingleEffect from '@/components/templates/SingleEffect.vue'

export default {
    name: 'Practice',
    props: ['kwargs'],
    components: { SingleEffect },
}
</script>
