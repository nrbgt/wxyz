import CodeMirror from 'codemirror';

import { DOMWidgetView } from '@jupyter-widgets/base';
import { TextareaModel } from '@jupyter-widgets/controls';

import { NAME, VERSION } from '..';

import { Mode } from '@jupyterlab/codemirror';

const EDITOR_CLASS = 'jp-WXYZ-Editor';

const WATCHED_OPTIONS = ['mode', 'theme'];

export class EditorModel extends TextareaModel {
  static model_name = 'EditorModel';
  static model_module = NAME;
  static model_module_version = VERSION;
  static view_name = 'EditorView';
  static view_module = NAME;
  static view_module_version = VERSION;

  defaults() {
    return {
      ...super.defaults(),
      _model_name: EditorModel.model_name,
      _model_module: NAME,
      _model_module_version: VERSION,
      _view_name: EditorModel.view_name,
      _view_module: NAME,
      _view_module_version: VERSION,
      description: 'An Editor',
      icon_class: 'jp-EditIcon',
      mode: null,
      theme: null
    };
  }
}

export class EditorView extends DOMWidgetView {
  private _editor: CodeMirror.Editor = null as any;

  render() {
    super.render();
    this.pWidget.addClass(EDITOR_CLASS);
    this._editor = CodeMirror(this.el);
    this._editor.on('change', () => {
      this.model.set('value', this._editor.getValue());
      this.touch();
    });

    this.model.on('change:value', this.value_changed, this);

    const watchers = WATCHED_OPTIONS.map(opt => {
      const watcher = this.optionWatcher(opt);
      this.model.on(`change:${opt}`, watcher);
      return watcher;
    });

    setTimeout(() => {
      this._editor.refresh();
      this.value_changed();
      watchers.map(fn => fn());
    }, 1);
  }

  optionWatcher(attr: string) {
    return async () => {
      const value = this.model.get(attr);
      switch (attr) {
        case 'theme':
          import(`codemirror/theme/${value}.css`).catch(console.warn);
          break;
        case 'mode':
          Mode.ensure(value).catch(console.warn);
          break;
        default:
          break;
      }
      this._editor.setOption(attr, value);
      this._editor.refresh();
    };
  }

  value_changed() {
    if (this._editor.getValue() !== this.model.get('value')) {
      let value = this.model.get('value');
      if (typeof value !== 'string') {
        value = JSON.stringify(value, null, 2);
      }
      this._editor.setValue(value);
    }
  }
}
