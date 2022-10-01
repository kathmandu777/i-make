<template>
    <div>
        <div class="container">
            <label class="card" v-for="(choiceImagesPath, i) in choiceImagesPaths" :for="i" :key="i">
                <input type="radio" :id="i" name="select-image" :value="choiceImagesPath"
                    v-model="selectedChoiceImagesPath" v-on:change="confirm" />
                <img v-bind:src="choiceImagesPath" width="230" height="250" />
            </label>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Choice',
    data: function () {
        return {
            choiceImagesPaths: [],
            selectedChoiceImagesPath: "",
        }
    },
    methods: {
        async getChoiceImagesPaths() {
            this.choiceImagesPaths=await window.eel.get_choice_images()()
        },
        async confirm() {
            await window.eel.set_skin_color(27.0, 36.0, 100.0)() // TODO: 任意の色を指定できるように
            await window.eel.set_effect_image_from_path(this.selectedChoiceImagesPath)()
            await window.eel.start()
        }
    },
    mounted: function () {
        this.getChoiceImagesPaths()
    }
}
</script>

<style scoped>
.container {
    width: 100%;
    height: 100%;
    padding: 10px;
    display: flex;
    flex-direction: row;
    flex-wrap: wrap;
    align-content: center;
    justify-content: flex-start;
    gap: 10px;
}

.card {
    border: 1px solid #ccc;
    border-radius: 5px;
}

.card>input {
    display: none;
}

.card:has(input:checked) {
    border: 2px solid #000;
}
</style>
