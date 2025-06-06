import { app } from "../../scripts/app.js";

app.registerExtension({
    name: "ComfyUI.UniversalToolkit",
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        if (nodeData.name === "MultiBlankGenerator") {
            // 自定义节点UI
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                const result = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;
                
                // 添加节点说明
                this.help = "生成指定尺寸和比例的空白图像、mask和latent";
                
                return result;
            };
        }
    }
}); 