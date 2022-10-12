<template>
    <div>
        <div class="keypad">
            <img
                src="/dist/left.png"
                @click="updateXOffset(offsetDiff)"
                class="key-4 card"
                v-shortkey="[4]"
                @shortkey="updateXOffset(offsetDiff)"
                width="240"
                height="240"
            />
            <img
                src="/dist/right.png"
                @click="updateXOffset(-offsetDiff)"
                class="key-6 card"
                v-shortkey="[6]"
                @shortkey="updateXOffset(-offsetDiff)"
                width="240"
                height="240"
            />
            <img
                src="/dist/up.png"
                @click="updateYOffset(-offsetDiff)"
                class="key-8 card"
                v-shortkey="[8]"
                @shortkey="updateYOffset(-offsetDiff)"
                width="240"
                height="240"
            />
            <img
                src="/dist/down.png"
                @click="updateYOffset(offsetDiff)"
                class="key-2 card"
                v-shortkey="[2]"
                @shortkey="updateYOffset(offsetDiff)"
                width="240"
                height="240"
            />

            <img
                src="/dist/plus.png"
                @click="updateScale(scaleDiff)"
                class="key-plus card"
                v-shortkey="['+']"
                @shortkey="updateScale(scaleDiff)"
                width="240"
                height="240"
            />
            <img
                src="/dist/minus.png"
                @click="updateScale(-scaleDiff)"
                class="key-minus card"
                v-shortkey="['-']"
                @shortkey="updateScale(-scaleDiff)"
                width="240"
                height="240"
            />

            <img
                class="key-0 card"
                v-shortkey.once="[0]"
                @shortkey="goToMenu()"
                @click="goToMenu"
                src="/dist/home.png"
                width="480"
                height="240"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: 'Config',
    data: function () {
        return {
            offsetDiff: 3,
            scaleDiff: 0.05,
        }
    },
    methods: {
        async goToMenu() {
            await window.eel.stop()()
            this.$emit('update-component', 'Menu')
        },
        async updateXOffset(diff) {
            await window.eel.update_x_offset(diff)()
        },
        async updateYOffset(diff) {
            await window.eel.update_y_offset(diff)()
        },
        async updateScale(diff) {
            await window.eel.update_scale(diff)()
        },
        async startConfig() {
            await window.eel.start_config()
        },
    },
    mounted() {
        this.startConfig()
    },
}
</script>

<style scoped>
.keypad {
    display: grid;
    grid-template-columns: 240px 240px 240px 240px;
    grid-template-rows: 60px 240px 240px 240px 240px 60px;
    grid-template-areas:
        '. . . .'
        'key-7 key-8 key-9 key-minus'
        'key-4 key-5 key-6 key-plus'
        'key-1 key-2 key-3 key-enter'
        'key-0 key-0 key-dot key-enter'
        '. . . .';
}

.key-0 {
    grid-area: key-0;
}

.key-1 {
    grid-area: key-1;
}

.key-2 {
    grid-area: key-2;
}

.key-3 {
    grid-area: key-3;
}

.key-4 {
    grid-area: key-4;
}

.key-5 {
    grid-area: key-5;
}

.key-6 {
    grid-area: key-6;
}

.key-7 {
    grid-area: key-7;
}

.key-8 {
    grid-area: key-8;
}

.key-9 {
    grid-area: key-9;
}

.key-minus {
    grid-area: key-minus;
}

.key-plus {
    grid-area: key-plus;
}

.card {
    border-radius: 5px;
    display: block;
    padding: 0;
    margin: 5px;
}

.card > input {
    display: none;
}

.card:has(input:checked) {
    border: 2px solid lightgreen;
}
</style>
