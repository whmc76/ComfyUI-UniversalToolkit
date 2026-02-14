/**
 * 启用上下文菜单自动嵌套子目录
 * 参考 ComfyUI-Easy-Use 的 easyContextMenu.js 实现，仅移植路径嵌套逻辑，不含缩略图。
 */

import { app } from "../../scripts/app.js";

const SETTING_ID = "UniversalToolkit.ContextMenuNestSub";
const THRESHOLD = 10;

app.registerExtension({
    name: "UniversalToolkit.contextMenuNest",
    async setup(app) {
        app.ui.settings.addSetting({
            id: SETTING_ID,
            name: "启用上下文菜单自动嵌套子目录（不适用于 Nodes 2.0）",
            type: "boolean",
            defaultValue: true,
            tooltip: "仅在使用 LiteGraph Canvas 时生效；Nodes 2.0 下 combo 下拉不经过 ContextMenu，本功能不可用。",
        });

        const getEnabled = () => !!app.ui.settings.getSettingValue(SETTING_ID, true);
        const existingContextMenu = LiteGraph.ContextMenu;

        LiteGraph.ContextMenu = function (values, options) {
            // 方案一：验证 Nodes 2.0 下是否仍会调用此处（点击 combo 下拉时若出现 log 则补丁生效）
            console.log("UniversalToolkit contextMenu nest patch applied", values?.length);
            const enabled = getEnabled();
            if (
                !enabled ||
                (values?.length || 0) <= THRESHOLD ||
                !(options?.callback) ||
                values.some((i) => typeof i !== "string")
            ) {
                return existingContextMenu.apply(this, [...arguments]);
            }

            const compatValues = values;
            const originalValues = [...compatValues];
            const folders = {};
            const specialOps = [];
            const folderless = [];

            for (const value of compatValues) {
                const splitBy = value.indexOf("/") > -1 ? "/" : "\\";
                const valueSplit = value.split(splitBy);
                if (valueSplit.length > 1) {
                    const key = valueSplit.shift();
                    folders[key] = folders[key] || [];
                    folders[key].push(valueSplit.join(splitBy));
                } else if (value === "CHOOSE" || value.startsWith("DISABLE ")) {
                    specialOps.push(value);
                } else {
                    folderless.push(value);
                }
            }

            const foldersCount = Object.keys(folders).length;
            if (foldersCount === 0) {
                return existingContextMenu.apply(this, [...arguments]);
            }

            const oldCallback = options.callback;
            options.callback = null;
            const newCallback = (item, opts) => {
                if (["None", "无", "無", "なし"].includes(item.content)) {
                    oldCallback("None", opts);
                } else {
                    const full = originalValues.find((i) => i.endsWith(item.content));
                    oldCallback(full != null ? full : item.content, opts);
                }
            };

            const addContent = (content) => ({
                content,
                callback: newCallback,
            });

            const add_sub_folder = (folder, folderName) => {
                const subs = [];
                const less = [];
                const b = folder.map((name) => {
                    const _folders = {};
                    const splitBy = name.indexOf("/") > -1 ? "/" : "\\";
                    const valueSplit = name.split(splitBy);
                    if (valueSplit.length > 1) {
                        const key = valueSplit.shift();
                        _folders[key] = _folders[key] || [];
                        _folders[key].push(valueSplit.join(splitBy));
                    }
                    const subKeys = Object.keys(_folders);
                    if (subKeys.length > 0) {
                        const key = subKeys[0];
                        const val = _folders[key][0];
                        if (key && val) subs.push({ key, value: val });
                        else less.push(addContent(name));
                    } else {
                        less.push(addContent(name));
                    }
                    return addContent(name);
                });

                if (subs.length > 0) {
                    const subsObj = {};
                    subs.forEach((item) => {
                        subsObj[item.key] = subsObj[item.key] || [];
                        subsObj[item.key].push(item.value);
                    });
                    return [
                        ...Object.entries(subsObj).map((f) => ({
                            content: f[0],
                            has_submenu: true,
                            callback: () => {},
                            submenu: {
                                options: add_sub_folder(f[1], f[0]),
                            },
                        })),
                        ...less,
                    ];
                }
                return b;
            };

            const newValues = [];
            for (const [folderName, folder] of Object.entries(folders)) {
                newValues.push({
                    content: folderName,
                    has_submenu: true,
                    callback: () => {},
                    submenu: {
                        options: add_sub_folder(folder, folderName),
                    },
                });
            }
            newValues.push(...folderless.map((f) => addContent(f)));
            if (specialOps.length > 0) {
                newValues.push(...specialOps.map((f) => addContent(f)));
            }

            return existingContextMenu.call(this, newValues, options);
        };
        LiteGraph.ContextMenu.prototype = existingContextMenu.prototype;
    },
});
