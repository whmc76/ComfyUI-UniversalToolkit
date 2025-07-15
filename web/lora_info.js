import { app } from "../../scripts/app.js";
import { ComfyWidgets } from "../../scripts/widgets.js";
import { api } from '../../scripts/api.js';

app.registerExtension({
  name: "LoraInfo_UTK",
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    if (nodeData.name === "LoraInfo_UTK") {

      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        onNodeCreated ? onNodeCreated.apply(this, []) : undefined;

        this.baseModelWidget = ComfyWidgets["STRING"](this, "Base Model", ["STRING", { multiline: false }], app).widget;
        this.showValueWidget = ComfyWidgets["STRING"](
          this,
          "output",
          ["STRING", { multiline: true }],
          app,
        ).widget;
        this.metaInfoWidget = ComfyWidgets["STRING"](
          this,
          "meta_info",
          ["STRING", { multiline: true }],
          app,
        ).widget;

        const [loraNameWidget, baseModelWidget, outputWidget, metaInfoWidget] = this.widgets;

        loraNameWidget.callback = () => {
          const value = loraNameWidget.value;

          const body = new FormData();
          body.append("lora_name", value);
          api
            .fetchApi("/lora_info_utk", { method: "POST", body })
            .then((response) => response.json())
            .then((resp) => {
              if (resp.error) {
                // 显示错误信息
                baseModelWidget.value = "错误";
                outputWidget.value = `获取信息失败: ${resp.error}`;
                metaInfoWidget.value = "无法获取元数据";
              } else {
                // 正常显示信息
                baseModelWidget.value = resp.baseModel;
                outputWidget.value = resp.output;
                metaInfoWidget.value = resp.metaInfo;
              }
            })
            .catch((error) => {
              // 处理网络错误
              console.error("[LoraInfo_UTK] API调用失败:", error);
              baseModelWidget.value = "网络错误";
              outputWidget.value = "无法连接到服务器，请检查网络连接";
              metaInfoWidget.value = "无法获取元数据";
            });
        };
      }

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, [message]);
        try {
          this.showValueWidget.value = message.text[0];
          this.baseModelWidget.value = message.model[0];
          this.metaInfoWidget.value = message.metaInfo ? message.metaInfo[0] : "";
        } catch (error) {
          console.error("[LoraInfo_UTK] 更新界面时发生错误:", error);
          this.showValueWidget.value = "界面更新失败";
          this.baseModelWidget.value = "";
          this.metaInfoWidget.value = "";
        }
      }
    }
  },
}); 