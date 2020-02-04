import matplotlib.pyplot as plt
import numpy as np


class CiuObject:
    def __init__(self, ci, cu):
        self.ci = ci
        self.cu = cu

    @staticmethod
    def _determine_importance(ci):
        if ci < 0.25:
            return 'not important'
        if ci < 0.5:
            return 'important'
        if ci < 0.75:
            return 'very important'
        else:
            return 'highly important'

    @staticmethod
    def _determine_typicality(cu):
        if cu < 0.25:
            return 'not typical'
        if cu < 0.5:
            return 'unlikely'
        if cu < 0.75:
            return 'typical'
        else:
            return 'very typical'

    def plot(self, data):
        fig, ax = plt.subplots()
        feature_names = self.ci.keys()
        bar = ax.bar(feature_names, data)

        ax = bar[0].axes
        lim = ax.get_xlim() + ax.get_ylim()
        for bar in bar:
            bar.set_facecolor("none")
            x, y = bar.get_xy()
            width, height = bar.get_width(), bar.get_height()
            grad = np.atleast_2d(np.linspace(256 ** height, 1, 256 ** height)).T
            ax.imshow(grad, extent=[x, x + width, y, y + height], aspect="auto")
        ax.axis(lim)

        axes = plt.gca()
        axes.set_ylim([0, 1])
        axes.spines['top'].set_visible(False)
        axes.spines['right'].set_visible(False)
        axes.spines['bottom'].set_visible(False)
        axes.spines['left'].set_visible(False)
        plt.show()

    def plot_ci(self):
        plt.title('Contextual Importance')
        self.plot(self.ci.values())

    def plot_cu(self):
        plt.title('Contextual Utility')
        self.plot(self.cu.values())

    def text_explain(self):
        feature_names = self.ci.keys()

        explanation_texts = []
        for index, feature in enumerate(feature_names):
            importance = self._determine_importance(self.ci[feature])
            typicality = self._determine_typicality(self.cu[feature])
            ci = round(self.ci[feature] * 100, 2)
            cu = round(self.cu[feature] * 100, 2)
            explanation_text = f'The feature "{feature}", which is ' \
                               f'{importance} (CI={ci}%), is {typicality} ' \
                               f'for its class (CU={cu}%).'
            explanation_texts.append(explanation_text)

        return explanation_texts