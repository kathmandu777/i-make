<template>
    <div>
        <div class="keypad">
            <Choices
                :choiceList="palette"
                @update="confirm"
                class="choices-page"
            >
                <template v-slot:default="{ choice }">
                    <div
                        class="color-sample"
                        :style="{ backgroundColor: hsvToRgbCode(choice) }"
                    ></div>
                </template>
            </Choices>

            <img
                class="key-0 card"
                v-shortkey.once="[0]"
                @shortkey="goToMenu()"
                @click="goToMenu"
                src="/dist/home.png"
                width="400"
                height="200"
            />
        </div>
    </div>
</template>

<script>
import Choices from '@/components/templates/Choices.vue'
export default {
    name: 'SkinColor',
    data: function () {
        return {
            palette: [],
            selectedHSV: null,
        }
    },
    methods: {
        async getPalette() {
            this.palette = await window.eel.get_skin_palette()()
        },
        async confirm(hsv) {
            if (hsv) this.selectedHSV = hsv
            await window.eel.set_skin_color(this.selectedHSV)()
        },
        async goToMenu() {
            await window.eel.stop()()
            this.$emit('update-component', 'Menu')
        },
        async startSkinColor() {
            await window.eel.start_skin_color()
        },
        hsvToRgbCode(hsv) {
            var h = hsv.h / 60
            var s = hsv.s / 100
            var v = hsv.v / 100
            if (s == 0)
                return (
                    'rgb(' +
                    parseInt(v * 255) +
                    ',' +
                    parseInt(v * 255) +
                    ',' +
                    parseInt(v * 255) +
                    ')'
                )
            var rgb
            var i = parseInt(h)
            var f = h - i
            var v1 = v * (1 - s)
            var v2 = v * (1 - s * f)
            var v3 = v * (1 - s * (1 - f))
            switch (i) {
                case 0:
                case 6:
                    rgb = [v, v3, v1]
                    break
                case 1:
                    rgb = [v2, v, v1]
                    break
                case 2:
                    rgb = [v1, v, v3]
                    break
                case 3:
                    rgb = [v1, v2, v]
                    break
                case 4:
                    rgb = [v3, v1, v]
                    break
                case 5:
                    rgb = [v, v1, v2]
                    break
            }
            return (
                'rgb(' +
                parseInt(rgb[0] * 255) +
                ',' +
                parseInt(rgb[1] * 255) +
                ',' +
                parseInt(rgb[2] * 255) +
                ')'
            )
        },
    },
    mounted: function () {
        this.getPalette()
        this.startSkinColor()
    },
    components: { Choices },
}
</script>

<style scoped>
.keypad {
    display: grid;
    grid-template-columns: 165px 210px 210px 210px 165px;
    grid-template-rows: 15px 210px 210px 210px 210px 210px 15px;
    grid-template-areas:
        '. . . . .'
        '. key-numlock key-slash key-asterisk .'
        '. key-7 key-8 key-9 .'
        '. key-4 key-5 key-6 .'
        '. key-1 key-2 key-3 .'
        '. key-0 key-0 key-dot .'
        '. . . . .';
}

.key-0 {
    grid-area: key-0;
}

.key-dot {
    grid-area: key-dot;
}

.choices-page {
    grid-row: 2/6;
    grid-column: 2/5;
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

.color-sample {
    width: 190px;
    height: 190px;
    border-radius: 60px;
    border: 2px solid #fff;
    margin: 4px 6px 6px 4px;
}
</style>
