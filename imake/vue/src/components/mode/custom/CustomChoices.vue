<template>
    <div>
        <div class="choices">
            <div v-if="!selectedFacepaint" class="choices-page">
                <Choices :choiceList="facepaints" @update="setFacepaint">
                    <template v-slot:default="{ choice }">
                        <img
                            :src="choice.thumbnail_path_for_frontend"
                            width="200"
                            height="200"
                        />
                    </template>
                </Choices>
            </div>
            <div v-else-if="!selectedColor" class="choices-page">
                <Choices :choiceList="hsvPalette" @update="setHSV">
                    <template v-slot:default="{ choice }">
                        <div
                            class="color-sample"
                            :style="{ backgroundColor: hsvToRgbCode(choice) }"
                        ></div>
                    </template>
                </Choices>
            </div>
        </div>
    </div>
</template>

<script>
import Choices from '@/components/templates/Choices.vue'
export default {
    name: 'CustomChoices',
    props: ['partKind'],
    data: function () {
        return {
            facepaints: [],
            hsvPalette: [],
            selectedFacepaint: null,
            selectedColor: null,
            page: 0,
        }
    },
    methods: {
        async getChoiceFacepaints() {
            this.facepaints = await window.eel.get_choice_facepaints_by_part(
                this.partKind.part_kind
            )()
        },
        async getHsvPalette() {
            this.hsvPalette = await window.eel.get_hsv_palette()()
        },
        setFacepaint(facepaint) {
            if (facepaint) this.selectedFacepaint = facepaint
            this.setFacepaintHSV()
        },
        setHSV(hsv) {
            if (hsv) this.selectedColor = hsv
            this.setFacepaintHSV()
        },
        setFacepaintHSV() {
            if (this.selectedFacepaint && this.selectedColor) {
                this.selectedFacepaint.hsv = this.selectedColor
                this.$emit('update', this.selectedFacepaint)
            }
        },
        async goToMenu() {
            await window.eel.stop()()
            this.$emit('update-component', 'Menu')
        },
        hsvToRgbCode(hsv) {
            var h = hsv.h / 60
            var s = hsv.s / 100
            var v = hsv.v / 100
            if (s == 0) return [v * 255, v * 255, v * 255]
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
    computed: {
        pageFacepaints() {
            return this.facepaints.slice(this.page * 9, this.page * 9 + 9)
        },
    },
    mounted: function () {
        this.getChoiceFacepaints()
        this.getHsvPalette()
    },
    components: { Choices },
}
</script>

<style scoped>
.choices {
    display: grid;
    grid-template-columns: 210px 210px 210px;
    grid-template-rows: 210px 210px 210px 210px;
    grid-template-areas:
        'key-numlock key-slush key-asterisk'
        'key-7 key-8 key-9'
        'key-4 key-5 key-6'
        'key-1 key-2 key-3';
}

.choices-page {
    grid-row: 1/5;
    grid-column: 1/4;
}

.color-sample {
    width: 190px;
    height: 190px;
    border-radius: 60px;
    margin: 4px 6px 6px 4px;
}
</style>
