<template>
    <SingleEffect :modeIconPath="kwargs.modeIconPath">Easy Mode</SingleEffect>
</template>

<script>
import SingleEffect from '@/components/shared/SingleEffect.vue'

export default {
    name: 'Easy',
    props: ['kwargs'],
    components: { SingleEffect },
}
</script>
