<template>
    <h1>Select Mode</h1>
    <ul id="mode">
        <li v-for="(name, i) in modes" :key="i">
            <button @click="setMode(name)">{{name}}</button>
        </li>
    </ul>
</template>

<script>
export default {
    name: 'Menu',
    data: function () {
        return {
            modes: []
        }
    },
    methods: {
        setMode(name) {
            window.eel.set_mode(name)()
            this.$router.push("/mode")
        },
        async getModes() {
            this.modes=await window.eel.get_mode_choices()()
        }
    },
    created: function () {
        this.getModes()
    }
}
</script>
