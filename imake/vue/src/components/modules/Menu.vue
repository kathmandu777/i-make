<template>
    <div class="half-HD">
        <h2 class="title">iMake!</h2>
        <img
            class="skin-color"
            v-on:click="goToSkinColor()"
            v-shortkey.once="['*']"
            @shortkey="goToSkinColor()"
            src="/dist/setting.png"
            width="160"
            height="160"
        />
        <img
            class="config"
            v-on:click="goToConfig()"
            v-shortkey.once="['backspace']"
            @shortkey="goToConfig()"
            src="/dist/spanner.png"
            width="160"
            height="160"
        />

        <div class="mode-list">
            <div v-for="(mode, index) in modes" :key="index" class="mode">
                <img
                    :src="mode.menu_image_path"
                    v-shortkey.once="[keys[index]]"
                    @shortkey="setMode(mode)"
                    @click="setMode(mode)"
                    role="button"
                    class="mode-button"
                />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Menu',
    data: function () {
        return {
            modes: [],
            keys: ['/', 8, 5, 2, 0], // 5モード前提
        }
    },
    methods: {
        setMode(mode) {
            const name = mode.name
            window.eel.set_mode(name)()
            this.$emit(
                'update-component',
                name.slice(0, 1).toUpperCase() + name.slice(1).toLowerCase(),
                {
                    modeIconPath: mode.icon_path,
                }
            )
        },
        async getModes() {
            this.modes = await window.eel.get_mode_choices()()
        },
        goToSkinColor() {
            this.$emit('update-component', 'SkinColor')
        },
        goToConfig() {
            this.$emit('update-component', 'Config')
        },
    },
    created: function () {
        this.getModes()
    },
}
</script>

<style scoped>
.half-HD {
    display: grid;
    grid-template-columns: 640px 160px 160px;
    grid-template-rows: 160px 920px;
    grid-template-areas:
        'title skin-color config'
        'select-mode select-mode select-mode';
}

.title {
    grid-area: title;
    font-size: 120px;
    line-height: 180px;
    margin: 0 20px;
    padding: 0;
}

.skin-color {
    grid-area: skin-color;
    margin: 0;
    padding: 0;
}

.config {
    grid-area: config;
    margin: 0;
    padding: 0;
}

.mode-list {
    grid-area: select-mode;
    display: flex;
    flex-direction: column;
    margin-top: 40px;
}

.mode {
    display: flex;
    flex-direction: row;
    align-items: center;
    margin: 10px;
}

.mode-button {
    width: 100%;
    height: auto;
    margin: 0;
}
</style>
