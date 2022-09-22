<template>
  <router-view></router-view>
</template>

<script>
export default {
  name: "App",
  mounted: function () {
    this.$router.push("/menu")
  },
}
</script>
