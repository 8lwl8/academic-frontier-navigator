/**
 * commitlint 配置
 * 依据：SPEC-03 §4 提交信息规范
 *
 * 安装：
 *   npm install --save-dev @commitlint/cli @commitlint/config-conventional husky
 *   npx husky init && echo 'npx --no -- commitlint --edit "$1"' > .husky/commit-msg
 *
 * 说明：架构书五(三)排除了生产级 CI/CD，此处仅做提交信息格式校验，
 *       不引入构建与部署流水线。
 */

export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    // type 受控词表（含本项目自定义的 data / prompt）
    'type-enum': [
      2,
      'always',
      [
        'feat',     // 新增功能
        'fix',      // 缺陷修复
        'docs',     // 文档变更
        'data',     // 数据文件变更（本项目特有）
        'prompt',   // 提示词变更（本项目特有）
        'refactor', // 重构（不改行为）
        'chore',    // 杂务
        'revert',   // 回滚
      ],
    ],

    // scope 受控词表
    'scope-enum': [
      2,
      'always',
      [
        'spec',   // docs/spec/
        'adr',    // docs/decisions/
        'kb',     // knowledge/
        'skill',  // skills/
        'prompt', // prompts/
        'web',    // web/
        'data',   // data/
        'config', // configs/
        'log',    // iteration-log/
        'repo',   // 仓库级
      ],
    ],

    // subject 规则：不超过 50 字，结尾不加句号
    'subject-max-length': [2, 'always', 50],
    'subject-full-stop': [2, 'never', '.'],
    'subject-empty': [2, 'never'],
    'subject-case': [0], // 中文无大小写概念，关闭

    // type 与 scope 必填
    'type-empty': [2, 'never'],
    'scope-empty': [1, 'never'], // 警告级：文档类提交可省略 scope

    // header 整体长度
    'header-max-length': [2, 'always', 80],

    // body 前必须空行
    'body-leading-blank': [2, 'always'],
    'footer-leading-blank': [2, 'always'],
  },

  // 自定义提示
  prompt: {
    questions: {
      type: {
        description: '选择提交类型',
        enum: {
          feat: { description: '新增功能', title: 'Features', emoji: '✨' },
          fix: { description: '缺陷修复', title: 'Bug Fixes', emoji: '🐛' },
          docs: { description: '文档变更', title: 'Documentation', emoji: '📝' },
          data: { description: '数据文件变更', title: 'Data', emoji: '🗂️' },
          prompt: { description: '提示词变更', title: 'Prompts', emoji: '💬' },
          refactor: { description: '重构', title: 'Refactors', emoji: '♻️' },
          chore: { description: '杂务', title: 'Chores', emoji: '🔧' },
          revert: { description: '回滚', title: 'Reverts', emoji: '⏪' },
        },
      },
      scope: {
        description: '选择影响范围',
        enum: {
          spec: { description: 'docs/spec/' },
          adr: { description: 'docs/decisions/' },
          kb: { description: 'knowledge/' },
          skill: { description: 'skills/' },
          prompt: { description: 'prompts/' },
          web: { description: 'web/' },
          data: { description: 'data/' },
          config: { description: 'configs/' },
          log: { description: 'iteration-log/' },
          repo: { description: '仓库级' },
        },
      },
      subject: {
        description: '简要描述变更内容（动词开头，不超过 50 字，结尾不加句号）',
      },
      body: {
        description: '详细说明变更的动机与内容',
      },
      isBreaking: {
        description: '是否为破坏性变更？',
      },
      issues: {
        description: '关联的待办或需求',
      },
    },
  },
};
