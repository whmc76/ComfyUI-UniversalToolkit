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

        const [loraNameWidget, baseModelWidget, outputWidget] = this.widgets;

        loraNameWidget.callback = () => {
          const value = loraNameWidget.value;

          const body = new FormData();
          body.append("lora_name", value);
          api
            .fetchApi("/lora_info_utk", { method: "POST", body })
            .then((response) => response.json())
            .then((resp) => {
              baseModelWidget.value = resp.baseModel;
              outputWidget.value = resp.output;
            });
        };
      }

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (message) {
        onExecuted?.apply(this, [message]);
        this.showValueWidget.value = message.text[0];
        this.baseModelWidget.value = message.model[0];
      }
    }
  },
}); 