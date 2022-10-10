<template>
    <div>
        <div class="keypad">
            <Choices
                :choiceList="facepaints"
                @update="confirm"
                class="choices-page"
            >
                <template v-slot:default="{ choice }">
                    <img
                        :src="choice.thumbnail_path_for_frontend"
                        width="195"
                        height="195"
                    />
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

            <img
                class="key-2 card"
                :src="modeIconPath"
                width="200"
                height="200"
            />
        </div>
    </div>
</template>

<script>
import Choices from '@/components/templates/Choices.vue'
export default {
    name: 'SingleEffect',
    props: ['modeIconPath'],
    data: function () {
        return {
            facepaints: [],
            selectedFacepaint: [],
        }
    },
    methods: {
        async getChoiceFacepaints() {
            this.facepaints = await window.eel.get_choice_facepaints()()
        },
        async confirm(facepaints) {
            if (facepaints) this.selectedFacepaint = facepaints
            await window.eel.set_effect_image_by_facepaints(
                this.selectedFacepaint
            )()
            await window.eel.start_rendering()
        },
        async goToMenu() {
            await window.eel.stop()()
            this.$emit('update-component', 'Menu')
        },
    },
    mounted: function () {
        this.getChoiceFacepaints()
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

.key-2 {
    grid-area: key-2;
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
</style>
