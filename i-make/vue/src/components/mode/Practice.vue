<template>
    <SingleEffect :modeIconPath="kwargs.modeIconPath">Practice Mode</SingleEffect>
</template>

<script>
import SingleEffect from '@/components/shared/SingleEffect.vue'

export default {
    name: "Practice",
    props: ["kwargs"],
    components: { SingleEffect }
}
</script>
